---
description: Create or update the project constitution from interactive or provided principle inputs.
handoffs:
  - label: Build Specification
    agent: speckit.specify
    prompt: Implement the feature specification based on the updated constitution. I want to build...
  - label: Implement Compliance Tasks
    agent: speckit.implement
    prompt: Implement constitution alignment tasks defined in tasks.md
scripts:
  sh: scripts/bash/resolve-template.sh constitution-template --json
  ps: scripts/powershell/resolve-template.ps1 constitution-template -Json
  py: scripts/python/resolve_template.py constitution-template --json
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Scope Guard & Plan-First Gate

This command's own work is limited to updating the project constitution itself and generating alignment tasks if needed.

- **Mandatory Plan Approval**: Before updating `.specify/memory/constitution.md` or generating follow-up tasks, you MUST outline the proposed principle amendments and obtain explicit user approval.
- Classify every part of the user input as either constitution content or a separate, non-governance intent.
- If the input includes feature implementation, code generation, refactoring, building, or deployment requests, you **MUST NOT** execute them directly. Extract them as deferred intents or append them as tasks.
- You **MUST NOT** modify application source files, components, tests, or deployment files in this command.

## Pre-Execution Checks

**Check for extension hooks (before constitution update)**:
- Check if `.specify/extensions.yml` exists in the project root.
- Filter out hooks where `enabled` is explicitly `false`.

## Outline

You are updating the project constitution at `.specify/memory/constitution.md`.

Follow this execution flow:

1. **Plan & Draft Review**:
   - Resolve template and load existing `.specify/memory/constitution.md` (if present).
   - Draft proposed changes and present the bump rationale and principle additions to the user.
   - **STOP and wait for user approval** before writing back the updated constitution.

2. **Required Dotfiles Principles (Mandatory)**:
   - Ensure the 6 non-negotiable principles are present:
     - I. **Espelhamento Obrigatório** (Dotfile config requires base package in `packages.json`).
     - II. **Instalador Completo** (Privileged `/etc/`, `/usr/` configs require explicit function in `utils.py` and call in `main.py`).
     - III. **Isolamento Root/Stow** (User configs strictly via GNU Stow; system configs strictly via installer scripts).
     - IV. **Idempotência** (Installer functions must be safe for continuous re-execution).
     - V. **Proibição de Segredos** (No SSH keys, tokens, or passwords in Git).
     - VI. **Higiene de Artefatos** (`.gitignore` & `.dotfilesignore` must cover caches, logs, and dumps).

3. **Write Constitution**:
   - Write updated document to `.specify/memory/constitution.md`.

4. **Task Generation & Append Protocol**:
   - If the new or updated principles require repository adjustments:
     - Check if `tasks.md` exists in the active feature directory or root.
     - Append a new section: `## Phase N: Constitution Alignment Gaps`.
     - Add checklist items in the format: `- [ ] T### [P?] [Const] Description with exact file path`.

5. **Completion Report & Commit Suggestion**:
   - Report version bump and summary of changes.
   - **Sugestão de Commit**: Fornecer sugestão de commit Conventional Commits (ex: `docs(constitution): amend project constitution to vX.Y.Z`).
   - Suggest handoff to `__SPECKIT_COMMAND_TASKS__` or `__SPECKIT_COMMAND_IMPLEMENT__` to execute alignment tasks.
