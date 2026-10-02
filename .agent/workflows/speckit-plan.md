---
description: Execute the implementation planning workflow using the plan template to generate design artifacts.
handoffs:
  - label: Create Tasks
    agent: speckit.tasks
    prompt: Break the plan into tasks
    send: true
  - label: Create Checklist
    agent: speckit.checklist
    prompt: Create a checklist for the following domain...
scripts:
  sh: scripts/bash/setup-plan.sh --json
  ps: scripts/powershell/setup-plan.ps1 -Json
  py: scripts/python/setup_plan.py --json
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Pre-Execution Checks

**Check for extension hooks (before planning)**:
- Check if `.specify/extensions.yml` exists in the project root.
- Filter out hooks where `enabled` is explicitly `false`.

## Outline

1. **Setup**: Run `{SCRIPT}` from repo root and parse JSON.
2. **Load context**: Read FEATURE_SPEC, `/memory/constitution.md`, and `.specify/memory/project-map.md` if available.
3. **Execute plan workflow**:
   - Fill Technical Context (OS/Distro, Stow, Package Managers, Privileges).
   - Phase 0: Generate `research.md`.
   - Phase 1: Generate `config-schema.md`, `contracts/`, `boot-validation.md`.

## Completion Report

Report branch, IMPL_PLAN path, generated artifacts, and provide:
- **Sugestão de Commit**: Fornecer sugestão de commit Conventional Commits (ex: `docs(plan): add technical implementation plan for [feature-name]`).

## Done When

- [ ] Plan workflow executed and design artifacts generated
- [ ] Completion reported to user with commit suggestion
