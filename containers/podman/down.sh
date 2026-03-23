#!/usr/bin/env bash
# Stop the APME pod and optionally wipe the database.
#
# Usage:
#   ./down.sh          # stop pod only
#   ./down.sh --wipe   # stop pod and delete the gateway database
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

echo "Stopping apme-pod..."
podman pod stop apme-pod 2>/dev/null || true
podman pod rm  apme-pod 2>/dev/null || true
echo "Pod stopped."

if [[ "${1:-}" == "--wipe" ]]; then
  CACHE_PATH="${APME_CACHE_HOST_PATH:-${XDG_CACHE_HOME:-$HOME/.cache}/apme}"
  DB_FILE="$CACHE_PATH/gateway.db"
  if [[ -f "$DB_FILE" ]]; then
    rm -f "$DB_FILE" "$DB_FILE-shm" "$DB_FILE-wal"
    echo "Wiped database: $DB_FILE"
  else
    echo "No database found at $DB_FILE"
  fi
fi
