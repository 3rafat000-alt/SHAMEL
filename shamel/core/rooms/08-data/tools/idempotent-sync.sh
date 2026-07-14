#!/usr/bin/env bash
# tool/dat/etl-engineer/idempotent-sync.sh — Generate idempotent ETL sync script
set -euo pipefail
SOFI_ROOT="${SOFI_ROOT:-$HOME/Desktop/Lorka}"
R="$(tput setaf 1)" G="$(tput setaf 2)" Y="$(tput setaf 3)" B="$(tput setaf 4)" X="$(tput sgr0)"

usage() { echo "Usage: $(basename $0) <PRJ-ID> <sync-name> [source]
Generate an idempotent ETL sync script with upsert logic.
  source  api|db|csv (default: api)
Example: etl-engineer/idempotent-sync.sh PRJ-SAKK orders api
--help"; exit 0; }

PRJ="$1"; SYNC="${2:-}"; SOURCE="${3:-api}"
[ "$PRJ" = "--help" ] && usage; [ -z "$SYNC" ] && echo "${R}Error: sync name required$X" && usage

PRJ_DIR="$SOFI_ROOT/projects/$PRJ"
SNAKE=$(echo "$SYNC" | tr '[:upper:]' '[:lower:]')
PASCAL=$(echo "$SYNC" | sed 's/_/ /g' | sed 's/\b\(.\)/\u\1/g' | tr -d ' ')
DIR="$PRJ_DIR/app/Console/Commands"
mkdir -p "$DIR"

CMD_FILE="$DIR/Sync${PASCAL}.php"
[ ! -f "$CMD_FILE" ] && cat > "$CMD_FILE" <<PHP
<?php
namespace App\Console\Commands;
use Illuminate\Console\Command;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Http;

class Sync${PASCAL} extends Command
{
    protected \$signature = 'sync:${SNAKE} {--force : Re-sync all records}';
    protected \$description = 'Idempotent ETL sync for ${PASCAL}';

    public function handle(): int
    {
        \$force = \$this->option('force');
        \$synced = 0; \$skipped = 0; \$failed = 0;

        \$records = \$this->fetchSource();
        \$bar = \$this->output->createProgressBar(count(\$records));
        \$bar->start();

        foreach (\$records as \$record) {
            try {
                \$existing = DB::table('${SNAKE}')->where('external_id', \$record['id'])->first();
                if (\$existing && !\$force) {
                    \$skipped++; \$bar->advance(); continue;
                }
                DB::table('${SNAKE}')->updateOrInsert(
                    ['external_id' => \$record['id']],
                    ['data' => json_encode(\$record), 'synced_at' => now()]
                );
                \$synced++;
            } catch (\Throwable \$e) {
                \$failed++; \$this->error(\$e->getMessage());
            }
            \$bar->advance();
        }
        \$bar->finish();
        \$this->newLine();
        \$this->info("Synced: \$synced, Skipped: \$skipped, Failed: \$failed");
        return 0;
    }

    private function fetchSource(): array
    {
        // @todo implement $SOURCE data source
        return [];
    }
}
PHP
echo "${G}Command:$X $CMD_FILE"

echo "${B}Done.$X Run: php artisan sync:${SNAKE}"
echo "Schedule in App\\Console\\Kernel: \\$schedule->command('sync:${SNAKE}')->hourly();"
