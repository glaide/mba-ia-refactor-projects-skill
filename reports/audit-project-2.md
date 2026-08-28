================================
ARCHITECTURE AUDIT REPORT
================================
Project: ecommerce-api-legacy
Stack:   Node.js + Express 4.18.2
Files:   3 analyzed | ~170 lines of code

## Summary
CRITICAL: 3 | HIGH: 4 | MEDIUM: 3 | LOW: 2

## Findings

### [CRITICAL] Hardcoded Production Secrets
File: src/utils.js:1-7
Description: Payment gateway key (pk_live_...), DB credentials, and SMTP user hardcoded in source.
Impact: Anyone with repo access gets live-equivalent secrets; breach risk if repo leaks.
Recommendation: Move all secrets to environment variables via config module.

### [CRITICAL] Admin Financial Report Without Authentication
File: src/AppManager.js:80-128
Description: GET /api/admin/financial-report is public with no token or role check.
Impact: Exposes revenue, course data, and student PII to any caller.
Recommendation: Add authentication middleware for admin routes.

### [CRITICAL] Credit Card Number Logged to Console
File: src/AppManager.js:45
Description: Raw PAN and payment gateway key logged during checkout processing.
Impact: PCI-DSS violation; card data harvestable from stdout/log aggregators.
Recommendation: Never log card numbers; use tokenization.

### [HIGH] Broken Password Hashing (badCrypto)
File: src/utils.js:17-23, used at src/AppManager.js:68
Description: badCrypto() concatenates base64 fragments — not cryptographic hashing.
Impact: Passwords trivially weak; offline attacks become trivial.
Recommendation: Replace with bcrypt or argon2.

### [HIGH] Existing-User Checkout Skips Password Verification
File: src/AppManager.js:40-41,73-75
Description: If email exists, checkout proceeds without checking pwd.
Impact: Knowing only an email allows enrollment/payment as that user.
Recommendation: Verify password for existing users before checkout.

### [HIGH] Unauthenticated Destructive Delete Endpoint
File: src/AppManager.js:131-137
Description: DELETE /api/users/:id has no auth; orphans enrollments and payments.
Impact: Anyone can delete users; data integrity breaks.
Recommendation: Add auth and cascade delete or soft delete.

### [HIGH] Raw Card Numbers in API Body
File: src/AppManager.js:33,45-46
Description: Full card number sent as JSON field; payment decided by cc.startsWith("4").
Impact: Increases PCI scope and fraud risk.
Recommendation: Use payment tokenization; never handle raw PAN.

### [MEDIUM] God Class — No Separation of Concerns
File: src/AppManager.js:4-141
Description: AppManager handles DB schema, seeding, routing, payment, reporting, and deletion.
Impact: Hard to test, extend, or refactor; violates SRP.
Recommendation: Split into models/, controllers/, routes/, config/.

### [MEDIUM] Financial Report Async Race Conditions
File: src/AppManager.js:89-127
Description: Nested forEach + callbacks mutate shared report counters asynchronously.
Impact: Nondeterministic completion; risk of incomplete reports under load.
Recommendation: Use async/await with sequential or Promise.all patterns.

### [MEDIUM] In-Memory Database — No Persistence
File: src/AppManager.js:7
Description: sqlite3.Database(':memory:') — all data vanishes on restart.
Impact: Unsuitable for real e-commerce; no durability or recovery.
Recommendation: Use file-based or external DB for production.

### [LOW] Cryptic API Field Names
File: src/AppManager.js:28-33
Description: Fields usr, eml, pwd, c_id instead of descriptive names.
Impact: Poor API contract; harder to integrate and maintain.
Recommendation: Use standard names (name, email, password, course_id).

### [LOW] No Global Error Handler or Security Headers
File: src/app.js:1-14
Description: No error middleware, security headers, CORS policy, or request logging.
Impact: Unhandled errors crash silently; missing security baseline.
Recommendation: Add errorHandler middleware and security headers.

================================
Total: 12 findings
================================

Phase 2 complete. Proceed with refactoring (Phase 3)? [y/n]
