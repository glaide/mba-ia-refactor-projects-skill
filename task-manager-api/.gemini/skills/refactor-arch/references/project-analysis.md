# Project Analysis Heuristics

## Language Detection

| Signal | Language |
|--------|----------|
| `requirements.txt`, `*.py`, `Pipfile` | Python |
| `package.json`, `*.js`, `*.ts` | JavaScript/TypeScript |
| `go.mod`, `*.go` | Go |
| `pom.xml`, `build.gradle`, `*.java` | Java |
| `Gemfile`, `*.rb` | Ruby |
| `composer.json`, `*.php` | PHP |

## Framework Detection

### Python
- `from flask import` → Flask (check version in requirements.txt)
- `from django` → Django
- `from fastapi import` → FastAPI
- `import sqlalchemy` / `Flask-SQLAlchemy` → ORM layer present

### Node.js
- `require('express')` / `import express` → Express
- `require('fastify')` → Fastify
- `@nestjs/core` → NestJS

## Architecture Mapping

| Pattern | Indicators |
|---------|------------|
| Flat monolith | All logic in 1-5 root files, no subdirectories |
| Partial MVC | `models/`, `routes/` exist but routes contain business logic |
| MVC | Separate models, views/routes, controllers with thin routes |
| God class | Single file/class > 200 lines handling DB + routes + business rules |

## Domain Inference

- Product/order/user routes → E-commerce
- Task/user/category routes → Task management
- Course/enrollment/checkout → LMS / EdTech
- Patient/appointment → Healthcare

## Database Detection

| Signal | Database |
|--------|----------|
| `sqlite3`, `:memory:`, `*.db` | SQLite |
| `psycopg2`, `postgresql://` | PostgreSQL |
| `pymongo`, `mongodb://` | MongoDB |
| `mysql`, `mysql2` | MySQL |

Extract table names from `CREATE TABLE`, SQLAlchemy models (`__tablename__`), or Mongoose schemas.

## File Counting

Include: source files in project root and `src/`, `models/`, `routes/`, `controllers/`.
Exclude: `node_modules/`, `__pycache__/`, `.venv/`, test files, config-only files, lock files.
