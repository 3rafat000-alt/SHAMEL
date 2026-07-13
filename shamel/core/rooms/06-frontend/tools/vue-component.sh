#!/usr/bin/env bash
# tool/fnt/vue-engineer/vue-component.sh — Scaffold Vue 3 component + Pinia store
set -euo pipefail
SOFI_ROOT="${SOFI_ROOT:-$HOME/Desktop/Lorka}"
R="$(tput setaf 1)" G="$(tput setaf 2)" Y="$(tput setaf 3)" B="$(tput setaf 4)" X="$(tput sgr0)"

usage() { echo "Usage: $(basename $0) <PRJ-ID> <ComponentName> [--store] [props...]
Scaffold a Vue 3 component with Composition API + script setup.
  --store    Also generate a Pinia store
  props      Comma-separated: title:string,count:number
Example: vue-component.sh PRJ-SAKK UserCard --store name:string,avatar:string
--help"; exit 0; }

PRJ="$1"; COMP="${2:-}"; shift 2 || true; HAS_STORE=""; PROPS=""
for a in "$@"; do [ "$a" = "--store" ] && HAS_STORE=1 || PROPS="$a"; done
[ "$PRJ" = "--help" ] && usage; [ -z "$COMP" ] && echo "${R}Error: ComponentName required$X" && usage

PRJ_DIR="$SOFI_ROOT/projects/$PRJ"
RES="$PRJ_DIR/resources/js"
KEBAB=$(echo "$COMP" | sed 's/\([A-Z]\)/-\L\1/g; s/^-//')
DIR="$RES/components"

mkdir -p "$DIR"

VUE_FILE="$DIR/${COMP}.vue"
if [ ! -f "$VUE_FILE" ]; then
  PROP_LINES=""
  if [ -n "$PROPS" ]; then
    IFS=',' read -ra P <<< "$PROPS"
    for p in "${P[@]}"; do
      pn=$(echo "$p" | cut -d: -f1)
      pt=$(echo "$p" | cut -d: -f2)
      PROP_LINES+="  ${pn}: { type: ${pt} as PropType<${pt}>, default: undefined },"$'\n'
    done
  fi

cat > "$VUE_FILE" <<VUE
<script setup lang="ts">
import { computed } from 'vue'
${HAS_STORE:+"import { use${COMP}Store } from '@/stores/${COMP}'"}
import type { PropType } from 'vue'

defineProps({
${PROP_LINES}})
const emit = defineEmits<{ (e: 'update', val: unknown): void }>()
${HAS_STORE:+"const store = use${COMP}Store()"}
</script>

<template>
  <div class="${KEBAB}">
    <slot />
  </div>
</template>

<style scoped>
.${KEBAB} { display: contents; }
</style>
VUE
echo "${G}Component:$X $VUE_FILE"
fi

# Pinia store
if [ -n "$HAS_STORE" ]; then
  STORE_DIR="$PRJ_DIR/resources/js/stores"
  mkdir -p "$STORE_DIR"
  STORE_FILE="$STORE_DIR/${COMP}.ts"
  [ ! -f "$STORE_FILE" ] && cat > "$STORE_FILE" <<TS
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const use${COMP}Store = defineStore('${KEBAB}', () => {
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function fetch(): Promise<void> {
    loading.value = true
    try { /* @todo fetch */ } catch (e: unknown) {
      error.value = e instanceof Error ? e.message : 'Unknown error'
    } finally { loading.value = false }
  }

  return { loading, error, fetch }
})
TS
  echo "${G}Store:$X $STORE_FILE"
fi

echo "${B}Done.$X Import: import ${COMP} from '@/components/${COMP}.vue'"
