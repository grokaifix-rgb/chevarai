#!/bin/bash
# Barcha sinovlar: ./tests/hammasi.sh
cd "$(dirname "$0")"
x=0
for f in test_*.py; do echo "== $f"; out=$(python3 "$f" 2>&1 | grep -v "^\[20"); echo "$out"; echo "$out" | grep -q "❌" && x=1; done
exit $x
