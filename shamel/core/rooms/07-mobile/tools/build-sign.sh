#!/usr/bin/env bash
# tool/mob/release-engineer/build-sign.sh — Build + sign for store
set -euo pipefail
SOFI_ROOT="${SOFI_ROOT:-$HOME/Desktop/Lorka}"
R="$(tput setaf 1)" G="$(tput setaf 2)" Y="$(tput setaf 3)" B="$(tput setaf 4)" X="$(tput sgr0)"

usage() { echo "Usage: $(basename $0) <PRJ-ID> <platform> [--dry-run]
Build and sign Flutter app for store submission.
  platform  android|ios
  --dry-run Only show commands without executing
Example: build-sign.sh PRJ-SAKK android
--help"; exit 0; }

PRJ="$1"; PLATFORM="${2:-}"; DRY="${3:-}"
[ "$PRJ" = "--help" ] && usage
[ -z "$PLATFORM" ] && echo "${R}Error: platform required (android|ios)$X" && usage
PRJ_DIR="$SOFI_ROOT/projects/$PRJ"
[ ! -d "$PRJ_DIR" ] && echo "${R}Error: project not found$X" && exit 1

echo "${B}=== Build + Sign: $PRJ ($PLATFORM) ===$X"
echo

run() {
  if [ "$DRY" = "--dry-run" ]; then echo "${Y}[DRY-RUN]$X $*"
  else echo "${G}Running:$X $*" && "$@"
  fi
}

case "$PLATFORM" in
  android)
    echo "${Y}Step 1: Clean$X"; run flutter clean
    echo "${Y}Step 2: Get packages$X"; run flutter pub get
    echo "${Y}Step 3: Build appbundle$X"
    run flutter build appbundle --release
    AAB=$(find "$PRJ_DIR/build/app/outputs/bundle/release" -name "*.aab" 2>/dev/null | head -1)
    if [ -f "$AAB" ]; then
      SIZE=$(stat -c%s "$AAB" 2>/dev/null || stat -f%z "$AAB" 2>/dev/null || echo 0)
      echo "${G}App bundle: $AAB ($((SIZE/1024/1024))MB)$X"
      echo "${Y}Sign with: jarsigner -keystore <key> $AAB <alias>$X"
    fi
    ;;
  ios)
    echo "${Y}Step 1: Clean$X"; run flutter clean
    echo "${Y}Step 2: Get packages$X"; run flutter pub get
    echo "${Y}Step 3: Build iOS archive$X"
    run flutter build ios --release --no-codesign 2>/dev/null || \
      echo "${Y}iOS build requires Xcode. Run manually:$X"
    echo "  flutter build ipa --release"
    echo "  xcrun xcodebuild -workspace ios/Runner.xcworkspace -scheme Runner -archivePath build/Runner.xcarchive archive"
    echo "  xcrun xcodebuild -exportArchive ..."
    ;;
  *)
    echo "${R}Error: platform must be android or ios$X"; exit 1
    ;;
esac

echo
echo "${B}Post-build:$X"
echo "  - Verify version in pubspec.yaml"
echo "  - Run flutter test"
echo "  - Upload to store console"
[ "$DRY" = "--dry-run" ] && echo "${Y}Dry-run complete — no files changed$X"
