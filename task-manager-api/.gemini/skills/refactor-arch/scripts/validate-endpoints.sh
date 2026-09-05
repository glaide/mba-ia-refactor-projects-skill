#!/usr/bin/env bash
set -euo pipefail

PORT="${1:-5000}"
BASE="http://localhost:${PORT}"

echo "Validating endpoints at ${BASE}..."

curl -sf "${BASE}/health" > /dev/null && echo "✓ /health"

if curl -sf "${BASE}/" > /dev/null 2>&1; then
  echo "✓ /"
fi

TOKEN=$(curl -sf -X POST "${BASE}/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"joao@email.com","password":"admin1234"}' | python3 -c "import sys,json; print(json.load(sys.stdin)['token'])")

AUTH_HEADER="Authorization: Bearer ${TOKEN}"

if curl -sf -H "${AUTH_HEADER}" "${BASE}/tasks" > /dev/null 2>&1; then
  echo "✓ /tasks"
fi

if curl -sf -H "${AUTH_HEADER}" "${BASE}/users" > /dev/null 2>&1; then
  echo "✓ /users"
fi

if curl -sf -H "${AUTH_HEADER}" "${BASE}/categories" > /dev/null 2>&1; then
  echo "✓ /categories"
fi

if curl -sf -H "${AUTH_HEADER}" "${BASE}/reports/summary" > /dev/null 2>&1; then
  echo "✓ /reports/summary"
fi

echo "Validation complete."
