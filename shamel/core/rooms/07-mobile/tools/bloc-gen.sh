#!/usr/bin/env bash
# tool/mob/state-engineer/bloc-gen.sh — Generate Bloc/Cubit with all states
set -euo pipefail
SOFI_ROOT="${SOFI_ROOT:-$HOME/Desktop/Lorka}"
R="$(tput setaf 1)" G="$(tput setaf 2)" Y="$(tput setaf 3)" B="$(tput setaf 4)" X="$(tput sgr0)"

usage() { echo "Usage: $(basename $0) <PRJ-ID> <BlocName> [--cubit]
Generate a Flutter Bloc with state class, events, and bloc implementation.
  --cubit   Generate a Cubit instead (simpler)
Example: bloc-gen.sh PRJ-SAKK Auth
--help"; exit 0; }

PRJ="$1"; BLOC="${2:-}"; MODE="${3:-bloc}"
[ "$PRJ" = "--help" ] && usage; [ -z "$BLOC" ] && echo "${R}Error: BlocName required$X" && usage

PRJ_DIR="$SOFI_ROOT/projects/$PRJ"
LIB="$PRJ_DIR/lib"
DIR="$LIB/bloc/${BLOC,,}"
mkdir -p "$DIR"
STATE="${BLOC}State"
EVENT="${BLOC}Event"

# State class
write_file() { [ ! -f "$1" ] && cat > "$1" && echo "${G}$2$X" || echo "${Y}Exists:$X $1"; }

write_file "$DIR/${STATE,,}.dart" "State class" <<DART
part of '${BLOC,,}_bloc.dart';

@immutable
sealed class $STATE {}

final class ${BLOC}Initial extends $STATE {}

final class ${BLOC}Loading extends $STATE {}

final class ${BLOC}Loaded extends $STATE {
  final String data;
  ${BLOC}Loaded(this.data);
}

final class ${BLOC}Error extends $STATE {
  final String message;
  ${BLOC}Error(this.message);
}
DART

if [ "$MODE" = "--cubit" ]; then
  # Cubit (simpler -- no events)
  write_file "$DIR/${BLOC,,}_cubit.dart" "Cubit" <<DART
import 'package:flutter_bloc/flutter_bloc.dart';
part '${STATE,,}.dart';

class ${BLOC}Cubit extends Cubit<$STATE> {
  ${BLOC}Cubit() : super(${BLOC}Initial());

  Future<void> load() async {
    emit(${BLOC}Loading());
    try {
      // @todo fetch data
      emit(${BLOC}Loaded('result'));
    } catch (e) {
      emit(${BLOC}Error(e.toString()));
    }
  }
}
DART
else
  # Full Bloc with events
  write_file "$DIR/${EVENT,,}.dart" "Event class" <<DART
part of '${BLOC,,}_bloc.dart';

@immutable
sealed class $EVENT {}

final class Load${BLOC} extends $EVENT {}

final class Refresh${BLOC} extends $EVENT {}
DART

  write_file "$DIR/${BLOC,,}_bloc.dart" "Bloc" <<DART
import 'package:flutter_bloc/flutter_bloc.dart';
part '${EVENT,,}.dart';
part '${STATE,,}.dart';

class ${BLOC}Bloc extends Bloc<$EVENT, $STATE> {
  ${BLOC}Bloc() : super(${BLOC}Initial()) {
    on<Load${BLOC}>((event, emit) async {
      emit(${BLOC}Loading());
      try {
        // @todo fetch data
        emit(${BLOC}Loaded('result'));
      } catch (e) {
        emit(${BLOC}Error(e.toString()));
      }
    });
  }
}
DART
fi

echo "${B}Done.$X Import: ${BLOC}Bloc() or ${BLOC}Cubit()"
