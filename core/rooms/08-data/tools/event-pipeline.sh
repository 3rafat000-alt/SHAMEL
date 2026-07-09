#!/usr/bin/env bash
# tool/dat/analytics-engineer/event-pipeline.sh — Scaffold analytics event + model
set -euo pipefail
SOFI_ROOT="${SOFI_ROOT:-$HOME/Desktop/Lorka}"
R="$(tput setaf 1)" G="$(tput setaf 2)" Y="$(tput setaf 3)" B="$(tput setaf 4)" X="$(tput sgr0)"

usage() { echo "Usage: $(basename $0) <PRJ-ID> <event-name> [fields...]
Scaffold analytics event class, migration, and Eloquent model.
  event-name  e.g., page_view, button_click, api_call
  fields      Comma-separated: user_id,page,referrer
Example: event-pipeline.sh PRJ-SAKK page_view user_id,page,duration_ms
--help"; exit 0; }

PRJ="$1"; EVENT="${2:-}"; shift 2 2>/dev/null || true
FIELDS="${*:-event_data}"
[ "$PRJ" = "--help" ] && usage; [ -z "$EVENT" ] && echo "${R}Error: event name required$X" && usage

PRJ_DIR="$SOFI_ROOT/projects/$PRJ"
SNAKE=$(echo "$EVENT" | tr '[:upper:]' '[:lower:]')
PASCAL=$(echo "$EVENT" | sed 's/_/ /g' | sed 's/\b\(.\)/\u\1/g' | tr -d ' ')

# Model
MODEL_DIR="$PRJ_DIR/app/Models/Analytics"
mkdir -p "$MODEL_DIR"
MODEL_FILE="$MODEL_DIR/${PASCAL}.php"
[ ! -f "$MODEL_FILE" ] && cat > "$MODEL_FILE" <<PHP
<?php
namespace App\Models\Analytics;
use Illuminate\Database\Eloquent\Model;
class ${PASCAL} extends Model
{
    protected \$table = 'analytics_${SNAKE}';
    protected \$fillable = ['${FIELDS//,/', '}'];
    protected \$casts = ['occurred_at' => 'datetime'];
}
PHP
echo "${G}Model:$X $MODEL_FILE"

# Migration
MIGR_DIR="$PRJ_DIR/database/migrations"
mkdir -p "$MIGR_DIR"
MIGR_FILE="$MIGR_DIR/$(date +%Y_%m_%d)_000000_create_analytics_${SNAKE}_table.php"
[ ! -f "$MIGR_FILE" ] && cat > "$MIGR_FILE" <<PHP
<?php
use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;
return new class extends Migration
{
    public function up(): void
    {
        Schema::create('analytics_${SNAKE}', function (Blueprint \$table) {
            \$table->id();
            \$${SNAKE}_fields = ['${FIELDS//,/\', \'}'];
            foreach (\$${SNAKE}_fields as \$field) {
                \$table->string(\$field)->nullable();
            }
            \$table->timestamp('occurred_at')->useCurrent();
            \$table->timestamps();
        });
    }
    public function down(): void { Schema::dropIfExists('analytics_${SNAKE}'); }
};
PHP
echo "${G}Migration:$X $MIGR_FILE"

echo "${B}Done.$X Dispatch: ${PASCAL}::create([...])"
