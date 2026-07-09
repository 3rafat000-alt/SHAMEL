#!/usr/bin/env bash
# tool/ops/cost-optimizer/cost-report.sh — Infrastructure cost analysis
set -euo pipefail
SOFI_ROOT="${SOFI_ROOT:-$HOME/Desktop/Lorka}"
RED=$(tput setaf 1); GREEN=$(tput setaf 2); YELLOW=$(tput setaf 3); BLUE=$(tput setaf 4); RESET=$(tput sgr0)

usage() { echo "Usage: $(basename "$0") [--prj PRJ-ID] [--provider aws|gcp|do|all] [--budget monthly_usd] [--output report.md]"; exit 0; }
PRJ=""; PROVIDER="all"; BUDGET=""; OUTPUT=""
while [[ $# -gt 0 ]]; do case "$1" in --prj) PRJ="$2"; shift2 ;; --provider) PROVIDER="$2"; shift2 ;; --budget) BUDGET="$2"; shift2 ;; --output) OUTPUT="$2"; shift2 ;; --help|-h) usage ;; *) usage ;; esac; shift; done

echo "${BLUE}[cost-report]${RESET} Infrastructure cost analysis for ${PRJ:-workspace}"; echo ""

declare -A costs
costs[aws_compute]=0
costs[aws_storage]=0
costs[aws_network]=0
costs[gcp_compute]=0
costs[gcp_storage]=0
costs[do_droplets]=0

detect_resources() {
  local dir="$1"
  # Count compute hints in docker-compose, k8s, terraform
  if [[ -f "$dir/docker-compose.yml" ]]; then
    local svc_count
    svc_count=$(grep -c "image:" "$dir/docker-compose.yml" 2>/dev/null || echo 0)
    costs[aws_compute]=$((costs[aws_compute] + svc_count * 15))
    costs[gcp_compute]=$((costs[gcp_compute] + svc_count * 14))
    costs[do_droplets]=$((costs[do_droplets] + svc_count * 12))
  fi
  # Storage hints
  local vol_count
  vol_count=$(grep -c "volumes:" "$dir/docker-compose.yml" 2>/dev/null || echo 0)
  costs[aws_storage]=$((costs[aws_storage] + vol_count * 10))
  costs[gcp_storage]=$((costs[gcp_storage] + vol_count * 9))
  # Count DB instances
  local db_count
  db_count=$(grep -c "DB_HOST\|database.*host\|pgsql\|mysql" "$dir/.env" "$dir/.env.*" 2>/dev/null || echo 0)
  costs[aws_storage]=$((costs[aws_storage] + db_count * 50))
  costs[gcp_storage]=$((costs[gcp_storage] + db_count * 45))
}

# Terraform cost estimation
estimate_terraform() {
  local tf_files
  tf_files=$(find "$1" -name "*.tf" -not -path "*/vendor/*" -not -path "*/.terraform/*" 2>/dev/null || true)
  if [[ -n "$tf_files" ]]; then
    local instance_count
    instance_count=$(grep -c "aws_instance\|google_compute_instance\|digitalocean_droplet" $tf_files 2>/dev/null || echo 0)
    costs[aws_compute]=$((costs[aws_compute] + instance_count * 30))
    costs[gcp_compute]=$((costs[gcp_compute] + instance_count * 28))
    costs[do_droplets]=$((costs[do_droplets] + instance_count * 24))
  fi
}

if [[ -n "$PRJ" ]]; then
  detect_resources "$SOFI_ROOT/projects/$PRJ"
  estimate_terraform "$SOFI_ROOT/projects/$PRJ"
else
  for d in "$SOFI_ROOT/projects"/*/; do
    [[ -d "$d" ]] && detect_resources "$d" && estimate_terraform "$d"
  done
  detect_resources "$SOFI_ROOT"
  estimate_terraform "$SOFI_ROOT"
fi

total=0
print_provider() {
  local provider="$1" compute="$2" storage="$3" extra="$4"
  echo "  $provider:"
  echo "    Compute: \$$compute/mo"
  echo "    Storage: \$$storage/mo"
  echo "    $extra"
  local sub=$((compute + storage))
  total=$((total + sub))
}

if [[ "$PROVIDER" == "all" || "$PROVIDER" == "aws" ]]; then
  print_provider "AWS" "${costs[aws_compute]}" "${costs[aws_storage]}" "Network: \$${costs[aws_network]}/mo"
fi
if [[ "$PROVIDER" == "all" || "$PROVIDER" == "gcp" ]]; then
  print_provider "GCP" "${costs[gcp_compute]}" "${costs[gcp_storage]}" ""
fi
if [[ "$PROVIDER" == "all" || "$PROVIDER" == "do" ]]; then
  print_provider "DigitalOcean" "${costs[do_droplets]}" "0" ""
fi

echo ""
echo "  ${BLUE}Estimated total: \$$total/mo${RESET}"
if [[ -n "$BUDGET" ]]; then
  if [[ $total -le $BUDGET ]]; then
    echo "  ${GREEN}✓ Within budget (\$$BUDGET)${RESET}"
  else
    echo "  ${RED}✗ Over budget (\$$BUDGET) by \$$((total - BUDGET))${RESET}"
  fi
fi

if [[ -n "$OUTPUT" ]]; then
  {
    echo "# Cost Report: ${PRJ:-workspace}"
    echo "Date: $(date -Iseconds)"
    echo "Estimated total: \$$total/mo"
  } > "$OUTPUT"
  echo "${BLUE}[cost-report] Report written to $OUTPUT${RESET}"
fi
echo "${GREEN}[cost-report] Done.${RESET}"
