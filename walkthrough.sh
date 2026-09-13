#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")/web"
case "${1:-start}" in
  start)
    if [[ ! -f dist/client/index.html ]]; then
      [[ -d node_modules ]] || npm ci
      npm run build
    fi
    exec node serve.mjs
    ;;
  build)
    [[ -d node_modules ]] || npm ci
    exec npm run build
    ;;
  dev)
    [[ -d node_modules ]] || npm ci
    exec npm run dev -- --hostname 127.0.0.1 --port "${PORT:-5173}"
    ;;
  test)
    [[ -d node_modules ]] || npm ci
    exec npm test
    ;;
  *) printf 'Usage: %s [start|build|dev|test]\n' "$0" >&2; exit 2 ;;
esac
