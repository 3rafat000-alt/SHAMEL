#!/usr/bin/env bash
# tool/bck/domain-engineer/service-gen.sh — Generate service class with interface
set -euo pipefail
SOFI_ROOT="${SOFI_ROOT:-$HOME/Desktop/Lorka}"
R="$(tput setaf 1)" G="$(tput setaf 2)" Y="$(tput setaf 3)" B="$(tput setaf 4)" X="$(tput sgr0)"

usage() { echo "Usage: $(basename $0) <PRJ-ID> <ServiceName> [methods]
Generate a service interface + implementation with stub methods.
  methods  Comma-separated: process,validate,transform
Example: service-gen.sh PRJ-SAKK Payment process,validate,refund
--help"; exit 0; }

PRJ="$1"; NAME="${2:-}"; METHODS="${3:-execute}"
[ "$PRJ" = "--help" ] && usage; [ -z "$NAME" ] && echo "${R}Error: ServiceName required$X" && usage

PRJ_DIR="$SOFI_ROOT/projects/$PRJ"
SPATH="$PRJ_DIR/app/Services"
mkdir -p "$SPATH/Contracts"

IFS=',' read -ra M <<< "$METHODS"

# Interface
IFILE="$SPATH/Contracts/${NAME}Interface.php"
[ ! -f "$IFILE" ] && cat > "$IFILE" <<PHP
<?php
namespace App\Services\Contracts;
interface ${NAME}Interface
{
$(for m in "${M[@]}"; do echo "    public function $m(array \$data): array;"; done)
}
PHP
echo "${G}Interface:$X $IFILE"

# Implementation
SFILE="$SPATH/${NAME}Service.php"
[ ! -f "$SFILE" ] && cat > "$SFILE" <<PHP
<?php
namespace App\Services;
use App\Services\Contracts\${NAME}Interface;
class ${NAME}Service implements ${NAME}Interface
{
    public function __construct()
    {
        // Inject dependencies here
    }
$(for m in "${M[@]}"; do echo "
    public function $m(array \$data): array
    {
        // @todo implement $m
        return ['success' => true, 'method' => '$m', 'data' => \$data];
    }"; done)
}
PHP
echo "${G}Service:$X $SFILE"

# Bind in AppServiceProvider
PROV="$PRJ_DIR/app/Providers/AppServiceProvider.php"
if [ -f "$PROV" ] && ! grep -q "${NAME}Interface" "$PROV"; then
  echo "${Y}Add to $PROV:\$X"
  echo "  \$this->app->bind(\\App\\Services\\Contracts\\${NAME}Interface::class, \\App\\Services\\${NAME}Service::class);"
fi
echo "${G}Done.$X"
