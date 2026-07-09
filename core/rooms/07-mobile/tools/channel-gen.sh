#!/usr/bin/env bash
# tool/mob/platform-engineer/channel-gen.sh — Generate platform channel bridge
set -euo pipefail
SOFI_ROOT="${SOFI_ROOT:-$HOME/Desktop/Lorka}"
R="$(tput setaf 1)" G="$(tput setaf 2)" Y="$(tput setaf 3)" B="$(tput setaf 4)" X="$(tput sgr0)"

usage() { echo "Usage: $(basename $0) <PRJ-ID> <channel-name> [method]
Generate a Flutter MethodChannel bridge with Swift/Kotlin stubs.
  channel-name  e.g., device_info, biometric_auth
  method        e.g., getDeviceId, authenticate
Example: channel-gen.sh PRJ-SAKK biometric_auth authenticate
--help"; exit 0; }

PRJ="$1"; CHANNEL="${2:-}"; METHOD="${3:-call}"
[ "$PRJ" = "--help" ] && usage; [ -z "$CHANNEL" ] && echo "${R}Error: channel name required$X" && usage

PRJ_DIR="$SOFI_ROOT/projects/$PRJ"
LIB="$PRJ_DIR/lib"
SNAKE=$(echo "$CHANNEL" | sed 's/-/_/g')
PASCAL=$(echo "$CHANNEL" | sed 's/[-_]/ /g' | sed 's/\b\(.\)/\u\1/g' | tr -d ' ')

# Dart side
DART_DIR="$LIB/platform"
mkdir -p "$DART_DIR"
DART_FILE="$DART_DIR/${SNAKE}_channel.dart"
[ ! -f "$DART_FILE" ] && cat > "$DART_FILE" <<DART
import 'package:flutter/services.dart';

class ${PASCAL}Channel {
  static const _channel = MethodChannel('com.sofi/$SNAKE');

  static Future<Map<dynamic, dynamic>> $METHOD() async {
    try {
      final result = await _channel.invokeMethod('$METHOD');
      return Map<dynamic, dynamic>.from(result ?? {});
    } on PlatformException catch (e) {
      throw Exception('${PASCAL}Error: \${e.message}');
    }
  }
}
DART
echo "${G}Dart:$X $DART_FILE"

# iOS stub
IOS_DIR="$PRJ_DIR/ios/Runner"
if [ -d "$IOS_DIR" ]; then
  SWIFT_FILE="$IOS_DIR/${PASCAL}Bridge.swift"
  [ ! -f "$SWIFT_FILE" ] && cat > "$SWIFT_FILE" <<SWIFT
import Flutter

class ${PASCAL}Bridge {
  static func register(with registrar: FlutterPluginRegistrar) {
    let channel = FlutterMethodChannel(name: "com.sofi/$SNAKE", binaryMessenger: registrar.messenger())
    channel.setMethodCallHandler { (call, result) in
      switch call.method {
      case "$METHOD":
        // @todo implement native $METHOD
        result(["status": "ok"])
      default:
        result(FlutterMethodNotImplemented)
      }
    }
  }
}
SWIFT
  echo "${G}iOS:$X $SWIFT_FILE"
fi

# Android stub
ANDROID_DIR="$PRJ_DIR/android/app/src/main/kotlin"
if [ -d "$ANDROID_DIR" ]; then
  KT_FILE="$ANDROID_DIR/${PASCAL}Bridge.kt"
  [ ! -f "$KT_FILE" ] && cat > "$KT_FILE" <<KT
import io.flutter.embedding.engine.FlutterEngine
import io.flutter.plugin.common.MethodChannel

class ${PASCAL}Bridge {
    companion object {
        private const val CHANNEL = "com.sofi/$SNAKE"
        fun register(flutterEngine: FlutterEngine) {
            MethodChannel(flutterEngine.dartExecutor.binaryMessenger, CHANNEL)
                .setMethodCallHandler { call, result ->
                    when (call.method) {
                        "$METHOD" -> {
                            // @todo implement native $METHOD
                            result.success(mapOf("status" to "ok"))
                        }
                        else -> result.notImplemented()
                    }
                }
        }
    }
}
KT
  echo "${G}Android:$X $KT_FILE"
fi

echo "${B}Done.$X Register bridge in MainActivity/AppDelegate"
