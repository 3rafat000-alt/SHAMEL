#!/usr/bin/env bash
# tool/bck/api-engineer/endpoint-scaffold.sh — Scaffold FormRequest+Controller+Service+Resource from OpenAPI
set -euo pipefail
SOFI_ROOT="${SOFI_ROOT:-$HOME/Desktop/Lorka}"
R="$(tput setaf 1)" G="$(tput setaf 2)" Y="$(tput setaf 3)" B="$(tput setaf 4)" X="$(tput sgr0)"

usage() { echo "Usage: $(basename $0) <PRJ-ID> <endpoint-name> [method]
Scaffold a Laravel API endpoint: FormRequest, Controller, Service, Resource, test.
  endpoint-name  e.g., create-user, list-orders
  method         GET|POST|PUT|DELETE (default: POST)
--help"; exit 0; }

PRJ="$1"; EP="${2:-}"; METHOD="${3:-POST}"
[ "$PRJ" = "--help" ] && usage; [ -z "$EP" ] && echo "${R}Error: endpoint name required$X" && usage

PRJ_DIR="$SOFI_ROOT/projects/$PRJ"
if [ ! -d "$PRJ_DIR/app" ]; then
  echo "${Y}No Laravel app at $PRJ_DIR — creating stub structure$X"
  mkdir -p "$PRJ_DIR"/{app/Http/{Controllers/API,Requests,Resources},app/Services,tests/Feature}
fi

# Convert kebab to PascalCase and camelCase
PASCAL=$(echo "$EP" | sed 's/-/ /g' | sed 's/\b\(.\)/\u\1/g' | tr -d ' ')
CAMEL=$(echo "$PASCAL" | sed 's/^./\l&/')
PLURAL=$(echo "$EP" | sed 's/-/ /g' | awk '{for(i=1;i<=NF;i++)$i=toupper(substr($i,1,1)) substr($i,2)}1' | tr -d ' ' | sed 's/$/s/')

echo "${B}Scaffolding: $PASCAL ($METHOD $EP)$X"

# FormRequest
REQ_FILE="$PRJ_DIR/app/Http/Requests/${PASCAL}Request.php"
if [ ! -f "$REQ_FILE" ]; then
cat > "$REQ_FILE" <<PHP
<?php
namespace App\Http\Requests;
use Illuminate\Foundation\Http\FormRequest;
class ${PASCAL}Request extends FormRequest
{
    public function authorize() { return true; }
    public function rules() { return []; }
}
PHP
echo "${G}Created:$X $REQ_FILE"
fi

# Controller
CTRL_FILE="$PRJ_DIR/app/Http/Controllers/API/${PASCAL}Controller.php"
if [ ! -f "$CTRL_FILE" ]; then
cat > "$CTRL_FILE" <<PHP
<?php
namespace App\Http\Controllers\API;
use App\Http\Controllers\Controller;
use App\Http\Requests\${PASCAL}Request;
use App\Http\Resources\${PLURAL}Resource;
use App\Services\${PASCAL}Service;
use Illuminate\Http\JsonResponse;
class ${PASCAL}Controller extends Controller
{
    public function __construct(private ${PASCAL}Service \$service) {}
    public function __invoke(${PASCAL}Request \$request): JsonResponse
    {
        \$result = \$this->service->execute(\$request->validated());
        return response()->json(new ${PLURAL}Resource(\$result));
    }
}
PHP
echo "${G}Created:$X $CTRL_FILE"
fi

# Service
SVC_FILE="$PRJ_DIR/app/Services/${PASCAL}Service.php"
if [ ! -f "$SVC_FILE" ]; then
cat > "$SVC_FILE" <<PHP
<?php
namespace App\Services;
class ${PASCAL}Service
{
    public function execute(array \$data): array
    {
        return ['success' => true, 'data' => \$data];
    }
}
PHP
echo "${G}Created:$X $SVC_FILE"
fi

# Resource
RES_FILE="$PRJ_DIR/app/Http/Resources/${PLURAL}Resource.php"
if [ ! -f "$RES_FILE" ]; then
cat > "$RES_FILE" <<PHP
<?php
namespace App\Http\Resources;
use Illuminate\Http\Resources\Json\JsonResource;
class ${PLURAL}Resource extends JsonResource
{
    public function toArray(\$request): array
    {
        return parent::toArray(\$request);
    }
}
PHP
echo "${G}Created:$X $RES_FILE"
fi

echo "${B}Done.$X Add routes: Route::$METHOD('$EP', [${PASCAL}Controller::class, '__invoke']);"
