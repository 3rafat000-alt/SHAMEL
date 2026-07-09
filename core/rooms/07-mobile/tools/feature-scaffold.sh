#!/usr/bin/env bash
# tool/mob/flutter-engineer/feature-scaffold.sh — Scaffold Flutter feature (data/domain/presentation)
set -euo pipefail
SOFI_ROOT="${SOFI_ROOT:-$HOME/Desktop/Lorka}"
R="$(tput setaf 1)" G="$(tput setaf 2)" Y="$(tput setaf 3)" B="$(tput setaf 4)" X="$(tput sgr0)"

usage() { echo "Usage: $(basename $0) <PRJ-ID> <feature-name>
Scaffold a Flutter feature with clean architecture layers:
  lib/features/<name>/{data,domain,presentation}
--help"; exit 0; }

PRJ="$1"; FEATURE="${2:-}"
[ "$PRJ" = "--help" ] && usage; [ -z "$FEATURE" ] && echo "${R}Error: feature name required$X" && usage

PRJ_DIR="$SOFI_ROOT/projects/$PRJ"
LIB="$PRJ_DIR/lib"
SNAKE=$(echo "$FEATURE" | sed 's/-/_/g')
PASCAL=$(echo "$FEATURE" | sed 's/[-_]/ /g' | sed 's/\b\(.\)/\u\1/g' | tr -d ' ')

create_dir() { mkdir -p "$1"; echo "${G}Dir:$X $1"; }
write_file() { [ ! -f "$1" ] && cat > "$1" && echo "${G}File:$X $1" || echo "${Y}Exists:$X $1"; }

create_dir "$LIB/features/$SNAKE/data/models"
create_dir "$LIB/features/$SNAKE/data/repositories"
create_dir "$LIB/features/$SNAKE/domain/entities"
create_dir "$LIB/features/$SNAKE/domain/repositories"
create_dir "$LIB/features/$SNAKE/domain/usecases"
create_dir "$LIB/features/$SNAKE/presentation/pages"
create_dir "$LIB/features/$SNAKE/presentation/widgets"
create_dir "$LIB/features/$SNAKE/presentation/providers"

# Entity
write_file "$LIB/features/$SNAKE/domain/entities/${PASCAL}.dart" <<DART
class ${PASCAL} {
  final String id;
  ${PASCAL}({required this.id});
  @override String toString() => '${PASCAL}(id: \$id)';
}
DART

# Repository interface
write_file "$LIB/features/$SNAKE/domain/repositories/${PASCAL}Repository.dart" <<DART
import '../entities/${PASCAL}.dart';
abstract class ${PASCAL}Repository {
  Future<${PASCAL}> getById(String id);
}
DART

# Use case
write_file "$LIB/features/$SNAKE/domain/usecases/Get${PASCAL}.dart" <<DART
import '../repositories/${PASCAL}Repository.dart';
class Get${PASCAL} {
  final ${PASCAL}Repository repo;
  Get${PASCAL}(this.repo);
  Future<void> call(String id) async {
    await repo.getById(id);
  }
}
DART

echo "${B}Done.$X Feature scaffold at lib/features/$SNAKE/"
echo "Add to app_router.dart: GoRoute(path: '/$SNAKE', builder: ...)"
