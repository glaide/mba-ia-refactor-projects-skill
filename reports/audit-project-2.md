================================
ARCHITECTURE AUDIT REPORT
================================
Project: ecommerce-api-legacy
Stack:   Node.js + Express 4.18.2
Files:   11 analyzed | ~264 lines of code

## Summary
CRITICAL: 0 | HIGH: 2 | MEDIUM: 2 | LOW: 1

## Findings

### [HIGH] Existing-User Checkout Skips Password Verification
File: src/controllers/checkoutController.js:27-32
Description: If email exists, checkout proceeds without checking pwd unless the client sends it. Omitting pwd allows enrollment/payment as that user.
Impact: Knowing only an email allows account takeover at checkout.
Recommendation: Require password for existing users before charge (playbook pattern 13).

### [HIGH] Raw Card Numbers in API Body
File: src/controllers/checkoutController.js:8,34; src/services/paymentService.js:3-10
Description: Full card number sent as JSON field `card`; payment decided by `cardNumber.startsWith("4")`.
Impact: Increases PCI scope and fraud risk; trivial to bypass approval logic.
Recommendation: Accept only `payment_token` from gateway; never handle raw PAN (playbook pattern 14).

### [MEDIUM] In-Memory Database — No Persistence
File: src/database.js:9
Description: `sqlite3.Database(':memory:')` — all data vanishes on restart.
Impact: Unsuitable for real e-commerce; no durability or recovery.
Recommendation: Use file-based or external DB for production.

### [MEDIUM] Cryptic API Field Names
File: src/controllers/checkoutController.js:8
Description: Fields `usr`, `eml`, `pwd`, `c_id`, `card` instead of descriptive names.
Impact: Poor API contract; harder to integrate and maintain.
Recommendation: Use standard names (name, email, password, course_id, payment_token).

### [LOW] No Security Headers or CORS Policy
File: src/app.js:10-16
Description: No helmet, CORS policy, or request logging middleware.
Impact: Missing security baseline for production deployment.
Recommendation: Add security headers middleware and explicit CORS config.

================================
Total: 5 findings
================================

Phase 2 complete. Proceed with refactoring (Phase 3)? [y/n]
