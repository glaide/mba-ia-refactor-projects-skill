---
name: refactor-arch
description: Analyzes, audits, and refactors backend projects to MVC architecture. Use when the user asks for refactor-arch, architectural audit, or MVC refactoring on any backend codebase.
---

# Refactor Architecture Skill

Execute three sequential phases. Read reference files from `references/` before each phase.

## Phase 1 — Project Analysis

1. Detect language from file extensions and dependency files (`requirements.txt`, `package.json`, `go.mod`, etc.).
2. Detect framework from imports and dependencies (Flask, Express, Django, FastAPI, etc.).
3. Identify entry point (`app.py`, `src/app.js`, `main.go`, etc.).
4. Map all routes/endpoints and count source files (exclude `node_modules`, `__pycache__`, tests).
5. Detect database type and tables from schema/migrations/DDL.
6. Infer application domain from route names and model entities.

Print this block:

```
================================
PHASE 1: PROJECT ANALYSIS
================================
Language:      <language>
Framework:     <framework> <version if found>
Dependencies:  <key deps>
Domain:        <domain description>
Architecture:  <current pattern description>
Source files:  <N> files analyzed
DB tables:     <table list>
================================
```

See [project-analysis.md](references/project-analysis.md) for detection heuristics.

## Phase 2 — Architecture Audit

1. Read [anti-patterns-catalog.md](references/anti-patterns-catalog.md).
2. Scan every source file against catalog detection signals.
3. Record each finding with exact `file:line` (or `file:start-end` for ranges).
4. Classify severity: CRITICAL → HIGH → MEDIUM → LOW.
5. Generate report using [audit-report-template.md](references/audit-report-template.md).

**STOP after printing the report.** Ask:

```
Phase 2 complete. Proceed with refactoring (Phase 3)? [y/n]
```

Do NOT modify any project file until the user confirms with `y` or equivalent.

## Phase 3 — Refactoring

Only after user confirmation:

1. Read [mvc-guidelines.md](references/mvc-guidelines.md) and [refactoring-playbook.md](references/refactoring-playbook.md).
2. Apply transformations matching detected anti-patterns.
3. Preserve all original HTTP routes, methods, and response contracts unless security requires removal (document removals in output).
4. Adapt scope to project maturity:
   - **Flat monolith:** full MVC restructure under `src/`.
   - **Partial layers:** consolidate existing folders; extract controllers from fat routes; wire unused services.
5. Extract config to environment variables (no hardcoded secrets).
6. Centralize error handling in middleware.
7. Use parameterized queries / ORM for all database access.

### Validation (mandatory)

After refactoring:

1. Install dependencies and start the application.
2. Verify boot succeeds with no import/runtime errors.
3. Hit original endpoints (health, CRUD, login, reports).
4. Confirm zero CRITICAL anti-patterns remain.

Print:

```
================================
PHASE 3: REFACTORING COMPLETE
================================
## New Project Structure
<tree output>

## Validation
  ✓ Application boots without errors
  ✓ All endpoints respond correctly
  ✓ Zero anti-patterns remaining
================================
```

Run `scripts/validate-endpoints.sh` if available for the detected stack.
