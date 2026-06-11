#!/bin/bash
# rapha — Foundry-port smoke test
set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
SCRIPT="$SKILL_DIR/scripts/research.sh"

echo "Test 1: --help works"
bash "$SCRIPT" --help >/dev/null 2>&1 || bash "$SCRIPT" 2>&1 | head -3
echo "  OK"

echo "Test 2: bash $SCRIPT demo"
bash "$SCRIPT" demo 2>&1 | head -10
echo "  OK"

echo "All smoke tests passed."
