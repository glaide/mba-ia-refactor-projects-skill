================================
ARCHITECTURE AUDIT REPORT
================================
Project: task-manager-api
Stack:   Python + Flask 3.0 + SQLAlchemy
Files:   14 analyzed | ~900 lines of code

## Summary
CRITICAL: 4 | HIGH: 3 | MEDIUM: 4 | LOW: 2

## Findings

### [CRITICAL] No Authentication on Any Endpoint
File: routes/task_routes.py:11, routes/user_routes.py:10, routes/report_routes.py:12
Description: All CRUD, search, stats, reports, and category endpoints are public.
Impact: Anyone can list/modify/delete users, tasks, and categories without credentials.
Recommendation: Add JWT or session middleware; enforce on all mutating routes.

### [CRITICAL] MD5 Password Hashing Without Salt
File: models/user.py:27-32
Description: set_password() and check_password() use unsalted MD5 (deprecated/insecure).
Impact: Rainbow tables crack hashes instantly on DB leak.
Recommendation: Replace with werkzeug.security or bcrypt.

### [CRITICAL] Password Hash Exposed in API Responses
File: models/user.py:16-25, used at routes/user_routes.py:33,85,129,207
Description: User.to_dict() includes password field returned on create, update, get, and login.
Impact: Attackers get password hashes from normal API calls for offline cracking.
Recommendation: Remove password from to_dict() serialization.

### [CRITICAL] Hardcoded Secret Key and Insecure Runtime Config
File: app.py:13,34
Description: SECRET_KEY='super-secret-key-123' hardcoded; debug=True, host='0.0.0.0'.
Impact: Fixed secret enables session forgery; debug exposes Werkzeug debugger (RCE risk).
Recommendation: Load config from environment; disable debug by default.

### [HIGH] Fake Auth Token With No Verification
File: routes/user_routes.py:207-211
Description: Login returns 'fake-jwt-token-' + str(user.id) with no signing or middleware validation.
Impact: False sense of security; any client can forge tokens for any user ID.
Recommendation: Implement signed JWT with expiry and validation middleware.

### [HIGH] Unauthenticated Privilege Escalation via Role
File: routes/user_routes.py:52,71-78,119-122
Description: POST/PUT /users accepts role (admin, manager) from anonymous callers.
Impact: Attacker creates or updates themselves to admin without checks.
Recommendation: Restrict role assignment to authenticated admin users.

### [HIGH] Hardcoded SMTP Credentials in Source
File: services/notification_service.py:9-10,17
Description: Email user/password (senha123) committed to repository.
Impact: Credential leak via VCS, logs, or forks.
Recommendation: Load SMTP config from environment variables.

### [MEDIUM] Service/Utils Layers Exist But Are Bypassed
File: services/notification_service.py, utils/helpers.py:57-108, routes/task_routes.py:86-154
Description: NotificationService never imported; helpers unused; routes duplicate validation.
Impact: False separation; refactors in one place won't apply elsewhere.
Recommendation: Wire services from controllers; use shared validation helpers.

### [MEDIUM] N+1 Queries in List Endpoints
File: routes/task_routes.py:14-58, routes/report_routes.py:30-68
Description: GET /tasks loads all tasks then User.query.get() and Category.query.get() per row.
Impact: Performance degrades linearly with data size.
Recommendation: Use SQLAlchemy joinedload for eager loading.

### [MEDIUM] Duplicated Business Logic
File: models/task.py:50-60, routes/task_routes.py:30-39, routes/user_routes.py:171-180
Description: Overdue detection copy-pasted in 5 places despite Task.is_overdue() method.
Impact: Bug fixes must be repeated; inconsistencies already possible.
Recommendation: Use Task.is_overdue() consistently; centralize in controller layer.

### [MEDIUM] Deprecated datetime.utcnow() Usage
File: routes/task_routes.py, models/task.py, app.py
Description: datetime.utcnow() used throughout (deprecated in Python 3.12+).
Impact: Future compatibility issues; naive datetimes cause timezone bugs.
Recommendation: Use datetime.now(timezone.utc) for timezone-aware datetimes.

### [LOW] Category CRUD Under Report Routes
File: routes/report_routes.py:157-223
Description: Category CRUD endpoints registered on report_bp instead of dedicated module.
Impact: Mixed concerns; confusing route organization.
Recommendation: Extract to category_routes.py or category_controller.py.

### [LOW] Side Effects at Import/Startup
File: app.py:30-31, seed.py:2
Description: db.create_all() runs on every app import; seed couples to full app factory.
Impact: Hard to test in isolation or run migrations properly.
Recommendation: Move schema init to explicit CLI command or migration tool.

================================
Total: 13 findings
================================

Phase 2 complete. Proceed with refactoring (Phase 3)? [y/n]
