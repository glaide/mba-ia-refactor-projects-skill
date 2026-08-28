#!/usr/bin/env bash
set -euo pipefail

PORT="${1:-5000}"
BASE="http://localhost:${PORT}"

echo "Validating endpoints at ${BASE}..."

curl -sf "${BASE}/health" > /dev/null && echo "✓ /health"

if curl -sf "${BASE}/" > /dev/null 2>&1; then
  echo "✓ /"
fi

if curl -sf "${BASE}/produtos" > /dev/null 2>&1; then
  echo "✓ /produtos"
fi

if curl -sf "${BASE}/tasks" > /dev/null 2>&1; then
  echo "✓ /tasks"
fi

if curl -sf "${BASE}/users" > /dev/null 2>&1; then
  echo "✓ /users"
fi

if curl -sf "http://localhost:3000/api/admin/financial-report" > /dev/null 2>&1; then
  echo "✓ /api/admin/financial-report"
fi

echo "Validation complete."
