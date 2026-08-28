================================
ARCHITECTURE AUDIT REPORT
================================
Project: code-smells-project
Stack:   Python + Flask 3.1.1
Files:   4 analyzed | ~800 lines of code

## Summary
CRITICAL: 4 | HIGH: 4 | MEDIUM: 3 | LOW: 2

## Findings

### [CRITICAL] Arbitrary SQL Execution Endpoint
File: app.py:59-78
Description: POST /admin/query executes any SQL string from request body with no authentication.
Impact: Full database compromise — read, modify, or delete all data.
Recommendation: Remove endpoint or restrict to authenticated read-only queries in dev.

### [CRITICAL] Unauthenticated Database Wipe
File: app.py:47-57
Description: POST /admin/reset-db deletes all rows from every table without auth.
Impact: Any caller can destroy all production data instantly.
Recommendation: Remove endpoint or protect with admin authentication.

### [CRITICAL] Systemic SQL Injection
File: models.py:47-49,109-110,126-128,280,289-297
Description: Queries built via string concatenation of user input (nome, email, senha, termo, categoria).
Impact: Attackers can bypass auth, exfiltrate data, or modify records.
Recommendation: Use parameterized queries with ? placeholders.

### [CRITICAL] Plaintext Password Storage
File: models.py:83,127-128 / database.py:76-78
Description: Passwords stored and matched as raw strings; seed users use weak passwords.
Impact: Credential theft from DB breach gives immediate account access.
Recommendation: Use werkzeug.security generate_password_hash/check_password_hash.

### [HIGH] Hardcoded SECRET_KEY Exposed in Health
File: app.py:7 / controllers.py:289
Description: SECRET_KEY "minha-chave-super-secreta-123" hardcoded and returned by /health.
Impact: Enables forgery of signed tokens if sessions are added later.
Recommendation: Load from environment variable; exclude from health response.

### [HIGH] Debug Mode Enabled in Production-like Config
File: app.py:8,88 / controllers.py:286-288
Description: DEBUG=True, app.run(debug=True), health reports debug=True and ambiente=producao.
Impact: Interactive debugger on errors; verbose stack traces leak internals.
Recommendation: Control debug via environment variable, default false.

### [HIGH] No Authentication on Business Endpoints
File: app.py:9 / controllers.py (all handlers)
Description: Products, users, orders, and sales report fully open; CORS allows all origins.
Impact: Anyone can list users with passwords, create/delete products, view all orders.
Recommendation: Add authentication middleware for protected routes.

### [HIGH] Password Field Returned in User List API
File: models.py:72-87 / controllers.py:128-132
Description: get_todos_usuarios() includes "senha" in every record returned by GET /usuarios.
Impact: Direct credential disclosure to any HTTP client.
Recommendation: Exclude password from API serialization.

### [MEDIUM] Global Singleton DB Connection
File: database.py:4-10
Description: One shared SQLite connection with check_same_thread=False across all requests.
Impact: Race conditions and locking errors under concurrent load.
Recommendation: Use connection per request or SQLAlchemy with proper pooling.

### [MEDIUM] Order Creation Lacks Atomic Transaction
File: models.py:133-169
Description: Multi-step inserts/updates with single commit but no rollback on mid-loop failure.
Impact: Partial state on crash — order without items or stock decremented without order.
Recommendation: Wrap in try/except with explicit rollback.

### [MEDIUM] N+1 Query Pattern
File: models.py:171-233
Description: For each order, separate queries for items and product names (3 cursors per order).
Impact: Performance degrades linearly with order volume.
Recommendation: Use JOIN queries to load items with orders in one query.

### [LOW] Broad Exception Handling
File: controllers.py:5-292
Description: except Exception swallows all errors; internal details returned as "erro": str(e).
Impact: Leaks schema/table names and query fragments to clients.
Recommendation: Centralize error handler; return generic messages.

### [LOW] Inconsistent Routing
File: app.py:11-30 vs app.py:47-78
Description: Most routes via add_url_rule + controllers; admin routes inline in app.py.
Impact: Maintenance friction; admin logic bypasses controller layer.
Recommendation: Move all routes to views/routes.py with controller delegation.

================================
Total: 13 findings
================================

Phase 2 complete. Proceed with refactoring (Phase 3)? [y/n]
