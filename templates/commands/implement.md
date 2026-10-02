---
description: Execute the implementation plan by processing and executing all tasks defined in tasks.md
scripts:
  sh: scripts/bash/check-prerequisites.sh --json --require-tasks --include-tasks
  ps: scripts/powershell/check-prerequisites.ps1 -Json -RequireTasks -IncludeTasks
  py: scripts/python/check_prerequisites.py --json --require-tasks --include-tasks
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Scope Guard & Plan-First Gate

This command executes code, configuration, and script modifications defined in `tasks.md`.

- **Mandatory Plan Approval**: Before executing any task or modifying source files, you MUST verify that an approved `plan.md` (or explicit user plan review) exists in context. If no plan exists or if tasks require major un-planned architectural changes, STOP and request running `__SPECKIT_COMMAND_PLAN__` or obtaining user plan approval first.

## Pre-Execution Checks

**Check for extension hooks (before implementation)**:
- Check if `.specify/extensions.yml` exists in the project root.
- Filter out hooks where `enabled` is explicitly `false`.

## Outline

1. Run `{SCRIPT}` from repo root and parse `FEATURE_DIR` and `AVAILABLE_DOCS` list.

2. **Verify Plan & Checklists Status**:
   - Confirm `plan.md` is loaded and approved.
   - Treat checklist markers as a read-only gate.

3. Load and analyze the implementation context (`tasks.md`, `plan.md`, `constitution.md`).

4. **Project Setup Verification**:
   - Check `.gitignore` and `.dotfilesignore`.
   - Validate Shell and Python scripts syntax (`bash -n`, `py_compile`).

5. Parse `tasks.md` and execute implementation in phases.
6. Mark completed tasks off as `[X]` in `tasks.md`.
7. **Completion Report & Commit Suggestion**:
   - Report final status with summary of completed work.
   - **Sugestão de Commit**: Fornecer sugestão de commit Conventional Commits (ex: `feat(dotfiles): implement [module/feature] configurations and setup routines`).
