#!/usr/bin/env bash
# tool/bck/queue-engineer/job-scaffold.sh — Generate queued job with retry/backoff
set -euo pipefail
SOFI_ROOT="${SOFI_ROOT:-$HOME/Desktop/Lorka}"
R="$(tput setaf 1)" G="$(tput setaf 2)" Y="$(tput setaf 3)" B="$(tput setaf 4)" X="$(tput sgr0)"

usage() { echo "Usage: $(basename $0) <PRJ-ID> <JobName> [queue-name] [tries]
Generate a queued job class with retry, backoff, and tags.
  JobName    e.g., ProcessPayment, SendWelcomeEmail
  queue-name default queue (default: default)
  tries      max attempts (default: 3)
--help"; exit 0; }

PRJ="$1"; JOB="${2:-}"; QUEUE="${3:-default}"; TRIES="${4:-3}"
[ "$PRJ" = "--help" ] && usage
[ -z "$JOB" ] && echo "${R}Error: JobName required$X" && usage

PRJ_DIR="$SOFI_ROOT/projects/$PRJ"
mkdir -p "$PRJ_DIR/app/Jobs"
FILE="$PRJ_DIR/app/Jobs/${JOB}.php"

if [ -f "$FILE" ]; then
  echo "${Y}Job already exists: $FILE$X"
  exit 0
fi

cat > "$FILE" <<PHP
<?php
namespace App\Jobs;
use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Bus\Dispatchable;
use Illuminate\Queue\InteractsWithQueue;
use Illuminate\Queue\SerializesModels;
class ${JOB} implements ShouldQueue
{
    use Dispatchable, InteractsWithQueue, Queueable, SerializesModels;

    public \$tries = $TRIES;
    public \$backoff = [2, 5, 10];

    public function __construct(
        public array \$data = []
    ) {
        \$this->onQueue('$QUEUE');
    }

    public function tags(): array
    {
        return ['${JOB,,}', 'queue:${QUEUE}'];
    }

    public function handle(): void
    {
        // @todo implement job logic
        // \$this->fail() or \$this->release(\$delay);
    }

    public function failed(\Throwable \$e): void
    {
        // @todo log or dispatch failure notification
    }
}
PHP

echo "${G}Job created:$X $FILE"
echo "${Y}Dispatch:$X ${JOB}::dispatch(\$data)"
