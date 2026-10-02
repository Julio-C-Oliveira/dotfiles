---
description: Identify underspecified areas in the current feature spec by asking up to 5 highly targeted clarification questions and encoding answers back into the spec.
handoffs:
  - label: Build Technical Plan
    agent: speckit.plan
    prompt: Create a plan for the spec. I am building with...
scripts:
   sh: scripts/bash/check-prerequisites.sh --json --paths-only
   ps: scripts/powershell/check-prerequisites.ps1 -Json -PathsOnly
   py: scripts/python/check_prerequisites.py --json --paths-only
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Pre-Execution Checks

**Check for extension hooks (before clarification)**:
- Check if `.specify/extensions.yml` exists in the project root.
- Filter out hooks where `enabled` is explicitly `false`.

## Outline

Goal: Detect and reduce ambiguity or missing decision points in the active feature specification and record the clarifications directly in the spec file.

1. Run `{SCRIPT}` from repo root once to get `FEATURE_DIR` and `FEATURE_SPEC`.
2. Load `/memory/constitution.md` and spec file.
3. Scan taxonomy categories and generate prioritized queue of clarification questions (max 5).
4. Sequential questioning loop (interactive).
5. Integrate answers into spec.md.
6. Re-validate Spec Quality Checklist if present.
7. Save updated spec file.

## Completion Report

Report completion with:
- Questions answered and sections updated.
- Checklist status summary.
- **Sugestão de Commit**: Fornecer sugestão de commit Conventional Commits (ex: `docs(spec): clarify requirements and edge cases for [feature-name]`).
- Next suggested command (`__SPECKIT_COMMAND_PLAN__`).

## Done When

- [ ] Spec ambiguities identified and clarifications integrated into spec file
- [ ] Completion reported to user with commit suggestion
