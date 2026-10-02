---
description: Perform a non-destructive cross-artifact consistency and quality analysis across spec.md, plan.md, and tasks.md after task generation.
handoffs:
  - label: Implement Remediation Tasks
    agent: speckit.implement
    prompt: Implement analysis remediation tasks defined in tasks.md
scripts:
  sh: scripts/bash/check-prerequisites.sh --json --require-spec --require-tasks --include-tasks
  ps: scripts/powershell/check-prerequisites.ps1 -Json -RequireSpec -RequireTasks -IncludeTasks
  py: scripts/python/check_prerequisites.py --json --require-spec --require-tasks --include-tasks
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Scope Guard & Plan-First Gate

This command performs cross-artifact analysis and offers optional remediation task generation.

- **Mandatory Plan Approval**: Analysis itself is read-only. If the user approves remediation of identified gaps, a clear Remediation Plan MUST be presented and approved before appending tasks to `tasks.md`.

## Outline

Follow this execution flow:

1. **Fase 0: Auditoria do Instalador (Dotfiles)**:
   - Check `packages.json`, `main.py`, `utils.py` for inconsistencies (`INS-01` to `INS-06`).

2. **Analysis Passes**:
   - Check Duplication, Ambiguity, Underspecification, Constitution Alignment, Coverage Gaps, Inconsistencies.

3. **Produce Analysis Report**:
   - Output table of findings and metrics.

4. **Task Generation & Append Protocol**:
   - If findings exist and user requests remediation:
     - Check if `tasks.md` exists.
     - Append a new section: `## Phase N: Analysis Remediation Tasks`.
     - Add checklist items in the format: `- [ ] T### [P?] [Analyze] Description with exact file path`.

5. **Handoff**:
   - Report findings summary and hand off to `__SPECKIT_COMMAND_IMPLEMENT__` if remediation tasks were appended.
