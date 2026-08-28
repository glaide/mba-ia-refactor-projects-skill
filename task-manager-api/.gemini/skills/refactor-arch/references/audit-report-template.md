# Audit Report Template

Use this exact structure for Phase 2 output:

```
================================
ARCHITECTURE AUDIT REPORT
================================
Project: <project-name>
Stack:   <language> + <framework>
Files:   <N> analyzed | ~<LOC> lines of code

## Summary
CRITICAL: <N> | HIGH: <N> | MEDIUM: <N> | LOW: <N>

## Findings

### [CRITICAL] <Anti-Pattern Name>
File: <path>:<line> or <path>:<start>-<end>
Description: <what was found>
Impact: <why it matters>
Recommendation: <specific fix>

### [HIGH] <Anti-Pattern Name>
File: <path>:<line>
Description: ...
Impact: ...
Recommendation: ...

(repeat for all findings, ordered CRITICAL → HIGH → MEDIUM → LOW)

================================
Total: <N> findings
================================

Phase 2 complete. Proceed with refactoring (Phase 3)? [y/n]
```

## Rules

- Every finding MUST have exact file and line reference
- Minimum 5 findings per project
- At least 1 CRITICAL or HIGH required
- Include deprecated API findings when applicable
- Do not begin Phase 3 until user confirms
