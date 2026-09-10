# Anti-Patterns Catalog

## 1. God Class / God Method — CRITICAL

**Signals:**
- Single class/file handles DB init, routing, business logic, and reporting
- File exceeds 200 lines with mixed responsibilities
- Python: one `models.py` with SQL + validation + DTO mapping for multiple domains
- Node: `AppManager` or similar owning everything

**Recommendation:** Split into models/, controllers/, routes/, config/

---

## 2. SQL Injection — CRITICAL

**Signals:**
- Python: string concatenation in SQL (`"WHERE id = " + str(id)`, f-strings with user input)
- Python: `"VALUES ('" + nome + "'"`
- Node: unparameterized template literals with `${userInput}` in queries
- Admin endpoint accepting raw SQL from request body

**Recommendation:** Use parameterized queries (`?` placeholders, `cursor.execute(sql, (param,))`) or ORM

---

## 3. Hardcoded Secrets — CRITICAL / HIGH

**Signals:**
- `SECRET_KEY = '...'` literal in source
- `paymentGatewayKey`, SMTP passwords, DB credentials in committed files
- API keys in `config` objects without `process.env` / `os.environ`

**Recommendation:** Move to environment variables; use `.env.example` without real values

---

## 4. Missing Authentication / Authorization — CRITICAL / HIGH

**Signals:**
- Admin/report/delete endpoints with no middleware check
- All CRUD endpoints publicly accessible
- Login exists but token never validated on subsequent requests
- Role assignment (`admin`) accepted from anonymous POST body
- Checkout with `else if (pwd)` — password optional for existing users
- Checkout proceeds for known email without identity verification before charge

**Recommendation:** Add auth middleware; protect sensitive routes; validate tokens; require password or session for existing-user checkout

---

## 5. Plaintext / Weak Password Storage — CRITICAL / HIGH

**Signals:**
- Passwords stored/compared as raw strings
- `hashlib.md5()` without salt
- Custom `badCrypto()` that is not a real hash function
- Seed data with plaintext passwords like `'123'`

**Recommendation:** Use `werkzeug.security` (Python) or `bcrypt` (Node); never return password/hash in API

---

## 6. Sensitive Data Exposure — HIGH

**Signals:**
- `to_dict()` or API responses include `password`, `senha`, `secret_key`
- Health endpoint returns internal config (debug flag, secret key, db path)
- Credit card numbers logged to console
- Request body accepts `card`, `cardNumber`, or raw PAN fields
- Payment approval via `startsWith` on card prefix (e.g. Visa = `"4"`)

**Recommendation:** Strip sensitive fields from serializers; sanitize health responses; use payment gateway tokens only

---

## 7. N+1 Queries — MEDIUM

**Signals:**
- Loop over parent records with separate query per child
- `User.query.get()` inside `for t in tasks`
- Nested callbacks each firing individual SELECT

**Recommendation:** Use JOINs, eager loading (`joinedload`), or aggregate queries

---

## 8. Missing Transaction Boundaries — MEDIUM

**Signals:**
- Multi-step inserts/updates with single commit at end but no rollback on failure
- Partial order creation possible on mid-loop error

**Recommendation:** Wrap in explicit transaction; rollback on any step failure

---

## 9. Blurred Layer Boundaries — MEDIUM

**Signals:**
- Routes contain validation + persistence + serialization
- Models contain HTTP-specific logic or discount tier business rules mixed with SQL
- Controllers print notification side effects instead of delegating to services
- Services/utils exist but are never imported

**Recommendation:** Routes → Controllers → Models/Services; each layer one responsibility

---

## 10. Deprecated / Insecure APIs — MEDIUM

**Signals:**
- `hashlib.md5()` for passwords (deprecated/insecure)
- `debug=True` with `host='0.0.0.0'` in production-like config
- SQLite callback hell instead of promises/async-await (Node)
- `datetime.utcnow()` (deprecated in Python 3.12+, prefer timezone-aware)
- Global mutable singleton DB connection with `check_same_thread=False`

**Recommendation:** Replace with modern equivalents; document migration in report

---

## 11. Broad Exception Handling — LOW

**Signals:**
- `except Exception as e:` returning `str(e)` to client
- Bare `except:` swallowing all errors
- DB delete errors ignored; always returns success

**Recommendation:** Catch specific exceptions; log internally; return generic client messages

---

## 12. Poor Naming / Magic Values — LOW

**Signals:**
- Cryptic API fields: `usr`, `eml`, `pwd`, `c_id`
- Magic numbers for discount tiers without named constants
- Misnamed files (`models.py` containing raw SQL, not ORM models)

**Recommendation:** Use descriptive names; extract constants to config
