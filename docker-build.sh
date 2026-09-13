#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
if [[ $# == 0 || ${1:-} == --help || ${1:-} == -h ]]; then
  cat <<'HELP'
Usage: ./docker-build.sh COMMAND
  list                    List room IDs
  room ROOM_ID [--site]    Build/bake one room; optionally compile the site
  all                     Generate all assets/previews, then compile the site
  site                    Compile the site from existing generated models

Outputs are written to this checkout. Container npm dependencies and cache
stay in .docker/. No server is started and nothing is published.
HELP
  exit 0
fi
export LOCAL_UID="$(id -u)" LOCAL_GID="$(id -g)"
mkdir -p .docker/node_modules .docker/npm-cache
docker compose build builder
docker compose run --rm --no-deps builder "$@"
