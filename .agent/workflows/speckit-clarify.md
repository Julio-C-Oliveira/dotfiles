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

Note: This clarification workflow is expected to run (and be completed) BEFORE invoking `__SPECKIT_COMMAND_PLAN__`.

Execution steps:

1. Run `{SCRIPT}` from repo root once to get `FEATURE_DIR` and `FEATURE_SPEC`.
2. **IF EXISTS**: Load `/memory/constitution.md` for project principles.
3. Load current spec file and scan taxonomy categories (Escopo Funcional, Dependências de Pacotes, Hardware & Ambiente, Fluxos de Teclado, Daemons/Background, Tratamento de Falhas, Ações Privilegiadas, Idempotência, Consistência com Instalador, Sinais de Conclusão).
4. Generate prioritized queue of candidate clarification questions (maximum 5).
5. Sequential questioning loop (interactive).
6. Integrate answers into spec.md.
7. Re-validate Spec Quality Checklist if present.
8. Save updated spec file.

## Completion Report

Report completion with questions answered, sections updated, checklist status, and next suggested command (`__SPECKIT_COMMAND_PLAN__`).

## Done When

- [ ] Spec ambiguities identified and clarifications integrated into spec file
- [ ] Completion reported to user
