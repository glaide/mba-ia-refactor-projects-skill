#!/usr/bin/env bash
set -euo pipefail

PORT="${1:-3000}"
BASE="http://localhost:${PORT}"
API_KEY="${ADMIN_API_KEY:-dev-admin-key}"

echo "Validating endpoints at ${BASE}..."

curl -sf -X POST "${BASE}/api/checkout" \
  -H "Content-Type: application/json" \
  -d '{"usr":"Test","eml":"validate@test.com","pwd":"1234","c_id":2,"payment_token":"tok_visa_ok"}' \
  > /dev/null && echo "✓ POST /api/checkout"

curl -sf "${BASE}/api/admin/financial-report" \
  -H "x-api-key: ${API_KEY}" \
  > /dev/null && echo "✓ GET /api/admin/financial-report"

echo "Validation complete."
