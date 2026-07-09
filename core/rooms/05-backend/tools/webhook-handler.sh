#!/usr/bin/env bash
# tool/bck/integration-engineer/webhook-handler.sh — Scaffold webhook handler with signature verification
set -euo pipefail
SOFI_ROOT="${SOFI_ROOT:-$HOME/Desktop/Lorka}"
R="$(tput setaf 1)" G="$(tput setaf 2)" Y="$(tput setaf 3)" B="$(tput setaf 4)" X="$(tput sgr0)"

usage() { echo "Usage: $(basename $0) <PRJ-ID> <provider> <event>
Scaffold webhook controller, verification middleware, and handler.
  provider   e.g., stripe, github, slack
  event      e.g., payment_intent.succeeded, push, message
Example: webhook-handler.sh PRJ-SAKK stripe payment_intent.succeeded
--help"; exit 0; }

PRJ="$1"; PROVIDER="${2:-}"; EVENT="${3:-}"
[ "$PRJ" = "--help" ] && usage
[ -z "$PROVIDER" ] && echo "${R}Error: provider required$X" && usage
[ -z "$EVENT" ] && echo "${R}Error: event required$X" && usage

PRJ_DIR="$SOFI_ROOT/projects/$PRJ"
PASCAL=$(echo "$PROVIDER" | sed 's/\b\(.\)/\u\1/g')
EVENT_CLASS=$(echo "$EVENT" | sed 's/\./_/g' | sed 's/\b\(.\)/\u\1/g' | sed 's/_//g')

mkdir -p "$PRJ_DIR"/{app/Http/Controllers/Webhooks,app/Http/Middleware,app/Events}

# Middleware
MDIR="$PRJ_DIR/app/Http/Middleware/Verify${PASCAL}Signature.php"
if [ ! -f "$MDIR" ]; then
cat > "$MDIR" <<PHP
<?php
namespace App\Http\Middleware;
use Closure;
use Illuminate\Http\Request;
class Verify${PASCAL}Signature
{
    public function handle(Request \$request, Closure \$next)
    {
        \$sig = \$request->header('X-${PASCAL^^}-Signature');
        \$secret = config('services.${PROVIDER,,}.webhook_secret');
        // @todo verify signature with provider's algorithm
        // if (!hash_equals(\$expected, \$sig)) abort(401);
        return \$next(\$request);
    }
}
PHP
echo "${G}Middleware:$X $MDIR"
fi

# Event
EVT_FILE="$PRJ_DIR/app/Events/${PASCAL}${EVENT_CLASS}.php"
if [ ! -f "$EVT_FILE" ]; then
cat > "$EVT_FILE" <<PHP
<?php
namespace App\Events;
use Illuminate\Foundation\Events\Dispatchable;
class ${PASCAL}${EVENT_CLASS}
{
    use Dispatchable;
    public function __construct(public array \$payload = []) {}
}
PHP
echo "${G}Event:$X $EVT_FILE"
fi

# Controller
CTRL="$PRJ_DIR/app/Http/Controllers/Webhooks/${PASCAL}WebhookController.php"
if [ ! -f "$CTRL" ]; then
cat > "$CTRL" <<PHP
<?php
namespace App\Http\Controllers\Webhooks;
use App\Http\Controllers\Controller;
use App\Events\\${PASCAL}${EVENT_CLASS};
use Illuminate\Http\Request;
class ${PASCAL}WebhookController extends Controller
{
    public function __invoke(Request \$request)
    {
        \$event = \$request->input('type', '${EVENT}');
        \${PASCAL,,}EventClass = "App\\\\Events\\\\${PASCAL}" . str_replace('.', '', ucwords(\$event, '.'));
        if (class_exists(\${PASCAL,,}EventClass)) {
            \${PASCAL,,}EventClass::dispatch(\$request->all());
        }
        return response()->json(['status' => 'received']);
    }
}
PHP
echo "${G}Controller:$X $CTRL"
fi

echo "${B}Done.$X Add route: Route::post('webhook/${PROVIDER,,}', [${PASCAL}WebhookController::class, '__invoke'])->middleware('verify.${PROVIDER,,}');"
