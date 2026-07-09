#!/usr/bin/env bash
# tool/mob/perf-profiler/perf-measure.sh — Capture before/after performance measurements
set -euo pipefail
SOFI_ROOT="${SOFI_ROOT:-$HOME/Desktop/Lorka}"
R="$(tput setaf 1)" G="$(tput setaf 2)" Y="$(tput setaf 3)" B="$(tput setaf 4)" X="$(tput sgr0)"

usage() { echo "Usage: $(basename $0) <PRJ-ID> <action> [label]
Flutter performance profiling actions:
  start       <label>  — Record baseline SHA + timestamp
  measure              — Run flutter build appbundle --profile and report size
  compare     <label>  — Compare current build size vs baseline
  report               — Generate performance report
Example: perf-measure.sh PRJ-SAKK start baseline-1
--help"; exit 0; }

PRJ="$1"; ACTION="${2:-}"; LABEL="${3:-}"
[ "$PRJ" = "--help" ] && usage; [ -z "$ACTION" ] && echo "${R}Error: action required$X" && usage
PRJ_DIR="$SOFI_ROOT/projects/$PRJ"
PERF_DIR="$PRJ_DIR/_context/perf"
mkdir -p "$PERF_DIR"

case "$ACTION" in
  start)
    SHA=$(git -C "$PRJ_DIR" rev-parse HEAD 2>/dev/null || echo "unknown")
    echo "{\"label\":\"$LABEL\",\"sha\":\"$SHA\",\"date\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"app_size_kb\":0,\"build_ms\":0}" \
      > "$PERF_DIR/baseline-${LABEL}.json"
    echo "${G}Baseline recorded:$X $LABEL @ $SHA"
    ;;
  measure)
    echo "${Y}Measuring build size...$X"
    APK=$(find "$PRJ_DIR/build" -name "*.apk" 2>/dev/null | head -1)
    AAB=$(find "$PRJ_DIR/build" -name "*.aab" 2>/dev/null | head -1)
    TARGET=""
    if [ -f "$APK" ]; then TARGET="$APK"
    elif [ -f "$AAB" ]; then TARGET="$AAB"
    fi
    if [ -n "$TARGET" ]; then
      SIZE=$(stat -c%s "$TARGET" 2>/dev/null || stat -f%z "$TARGET" 2>/dev/null || echo 0)
      KB=$((SIZE/1024))
      echo "${B}App size: ${KB}KB$X"
    else
      echo "${Y}No .apk or .aab found — run 'flutter build appbundle --profile' first$X"
    fi
    # Build time from flutter logs
    BUILD_LOG=$(find "$PRJ_DIR" -name "flutter_log*" -mmin -5 2>/dev/null | head -1)
    [ -n "$BUILD_LOG" ] && grep "Built\|Time elapsed" "$BUILD_LOG" | tail -3 || true
    ;;
  compare)
    [ -z "$LABEL" ] && echo "${R}Error: label required$X" && exit 1
    BASELINE="$PERF_DIR/baseline-${LABEL}.json"
    [ ! -f "$BASELINE" ] && echo "${R}Baseline not found:$X $BASELINE" && exit 1
    echo "${B}Baseline:$X $LABEL ($(grep -o '"sha":"[^"]*"' "$BASELINE" | cut -d'"' -f4))"
    # Current commit
    echo "${B}Current:$X $(git -C "$PRJ_DIR" rev-parse --short HEAD 2>/dev/null || echo '?')"
    # Look for size diff
    grep -o '"app_size_kb":[0-9]*' "$BASELINE" 2>/dev/null
    ;;
  report)
    echo "${B}=== Performance Report: $PRJ ===$X"
    echo "Date: $(date -u)"
    echo "Commit: $(git -C "$PRJ_DIR" rev-parse --short HEAD 2>/dev/null || echo '?')"
    echo "---"
    for b in "$PERF_DIR"/baseline-*.json; do
      [ -f "$b" ] && echo "Baseline: $(basename "$b" .json)" && grep -o '"sha":"[^"]*"' "$b" && echo
    done
    echo "${G}Report written to $PERF_DIR/report.md$X"
    ;;
esac
