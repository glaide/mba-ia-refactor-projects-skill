# MVC Architecture Guidelines

## Layer Responsibilities

| Layer | Responsibility | Must NOT |
|-------|---------------|----------|
| **Model** | Data access, queries, domain entities | Handle HTTP, parse request JSON |
| **View/Routes** | URL mapping, HTTP method binding | Contain business logic or SQL |
| **Controller** | Request validation, orchestration, response formatting | Execute raw SQL directly |
| **Config** | Environment variables, app settings | Contain business logic |
| **Middleware** | Cross-cutting: auth, errors, logging | Domain-specific rules |
| **App entry** | Composition root: wire layers, start server | Business logic |

## Python/Flask Target Structure

```
src/
├── config/settings.py
├── models/
│   └── <domain>_model.py
├── views/routes.py          # Blueprints or add_url_rule wiring
├── controllers/
│   └── <domain>_controller.py
├── middlewares/error_handler.py
└── database.py              # Connection factory (optional)
app.py                       # Composition root
```

## Node/Express Target Structure

```
src/
├── config/index.js
├── models/
│   └── <entity>Model.js
├── routes/
│   └── <resource>Routes.js
├── controllers/
│   └── <resource>Controller.js
├── middlewares/
│   ├── errorHandler.js
│   └── auth.js
└── app.js                   # Bootstrap + listen
```

## Partially Organized Projects (e.g. existing blueprints)

- Keep working folder structure where possible
- Extract fat route handlers into controllers
- Move validation to controllers or dedicated validators
- Wire existing but unused services
- Do NOT delete functional blueprints; thin them to delegate

## Security Baseline (all stacks)

- No hardcoded secrets
- Parameterized queries or ORM only
- Passwords hashed with industry-standard algorithm
- Sensitive fields excluded from API responses
- Admin endpoints protected or removed
- Debug mode off by default; controlled via env

## Error Handling

- Register global error handler middleware
- Return consistent JSON error shape: `{ "erro": "message" }` or `{ "error": "message" }`
- Log full errors server-side; never expose stack traces in production
