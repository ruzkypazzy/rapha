#!/bin/bash
# rapha — bash wrapper for the Python research assistant.
# Usage:
#   bash scripts/research.sh wallet <ADDRESS> [--chain mainnet|testnet]
#   bash scripts/research.sh token <TOKEN>
#   bash scripts/research.sh report <ADDRESS> <TOKEN>
#   bash scripts/research.sh demo

set -e
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$HERE/.."

CMD="${1:-}"
shift || true

if [ -z "$CMD" ]; then
  echo "Usage: bash scripts/research.sh {wallet|token|report|demo} [args...]"
  exit 1
fi

case "$CMD" in
  demo)
    python3 rapha.py demo
    ;;
  wallet|token|report)
    python3 rapha.py "$CMD" "$@"
    ;;
  *)
    echo "Unknown subcommand: $CMD"
    exit 1
    ;;
esac
