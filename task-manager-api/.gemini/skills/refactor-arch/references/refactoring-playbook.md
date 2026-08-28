# Refactoring Playbook

## 1. God Class → MVC Split

**Before (Node):**
```javascript
class AppManager {
  initDb() { /* schema + seed */ }
  setupRoutes(app) { /* all routes + business logic */ }
}
```

**After:**
```javascript
// src/app.js
const db = require('./database');
const checkoutRoutes = require('./routes/checkoutRoutes');
db.init();
app.use('/api', checkoutRoutes);

// src/controllers/checkoutController.js
async function checkout(req, res, next) {
  const result = await enrollmentModel.enroll(userId, courseId);
  res.json(result);
}
```

---

## 2. SQL Injection → Parameterized Queries

**Before (Python):**
```python
cursor.execute("SELECT * FROM usuarios WHERE email = '" + email + "'")
```

**After:**
```python
cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
```

---

## 3. Hardcoded Secrets → Environment Config

**Before:**
```python
app.config["SECRET_KEY"] = "minha-chave-super-secreta-123"
```

**After:**
```python
# src/config/settings.py
import os
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-key-change-me")
DEBUG = os.environ.get("DEBUG", "false").lower() == "true"
```

---

## 4. Plaintext Passwords → Secure Hashing

**Before:**
```python
cursor.execute("INSERT INTO usuarios ... VALUES (?, ?, ?)", (nome, email, senha))
```

**After:**
```python
from werkzeug.security import generate_password_hash, check_password_hash
hashed = generate_password_hash(senha)
cursor.execute("INSERT INTO usuarios ... VALUES (?, ?, ?)", (nome, email, hashed))
```

---

## 5. Password Exposure → Safe Serialization

**Before:**
```python
def to_dict(self):
    return {'id': self.id, 'email': self.email, 'password': self.password}
```

**After:**
```python
def to_dict(self):
    return {'id': self.id, 'email': self.email, 'role': self.role}
```

---

## 6. Fat Routes → Thin Routes + Controllers

**Before:**
```python
@task_bp.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    result = []
    for t in tasks:
        # 50 lines of serialization + N+1 queries
    return jsonify(result)
```

**After:**
```python
@task_bp.route('/tasks', methods=['GET'])
def get_tasks():
    return task_controller.list_tasks()

# controllers/task_controller.py
def list_tasks():
    tasks = task_model.get_all_with_relations()
    return jsonify([t.to_dict() for t in tasks]), 200
```

---

## 7. N+1 Queries → Eager Loading / JOINs

**Before:**
```python
for t in tasks:
    user = User.query.get(t.user_id)
```

**After:**
```python
from sqlalchemy.orm import joinedload
tasks = Task.query.options(joinedload(Task.user), joinedload(Task.category)).all()
```

---

## 8. Missing Transactions → Explicit Rollback

**Before:**
```python
for item in itens:
    cursor.execute("INSERT INTO itens_pedido ...")
    cursor.execute("UPDATE produtos SET estoque ...")
db.commit()
```

**After:**
```python
try:
    for item in itens:
        cursor.execute("INSERT INTO itens_pedido ...", (...))
        cursor.execute("UPDATE produtos SET estoque = estoque - ? WHERE id = ?", (...))
    db.commit()
except Exception:
    db.rollback()
    raise
```

---

## 9. Dangerous Admin Endpoints → Remove or Protect

**Before:**
```python
@app.route("/admin/query", methods=["POST"])
def executar_query():
    cursor.execute(request.json["sql"])
```

**After:** Remove endpoint entirely, or gate behind auth + allowlist of read-only queries in dev only.

---

## 10. Global Error Handler → Centralized Middleware

**Before:**
```python
except Exception as e:
    return jsonify({"erro": str(e)}), 500
```

**After:**
```python
# middlewares/error_handler.py
def register_error_handlers(app):
    @app.errorhandler(Exception)
    def handle_error(e):
        app.logger.exception(e)
        return jsonify({"erro": "Erro interno do servidor"}), 500
```

---

## 11. Callback Hell → Promises (Node)

**Before:**
```javascript
this.db.get("...", [], (err, row) => {
  this.db.run("...", [], (err) => {
    this.db.run("...", [], (err) => { res.json(...); });
  });
});
```

**After:**
```javascript
const { promisify } = require('util');
const dbGet = promisify(db.get.bind(db));
const row = await dbGet("SELECT ...", [id]);
```

---

## 12. Unused Service Layer → Wire Services

**Before:** `NotificationService` exists but routes never import it.

**After:**
```python
from services.notification_service import NotificationService
notifier = NotificationService()
notifier.notify_task_assigned(user, task)
```

Move SMTP credentials to environment variables when wiring.
