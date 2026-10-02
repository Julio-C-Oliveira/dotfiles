---
description: Create or update the feature specification from a natural language feature description.
handoffs:
  - label: Build Technical Plan
    agent: speckit.plan
    prompt: Create a plan for the spec. I am building with...
  - label: Clarify Spec Requirements
    agent: speckit.clarify
    prompt: Clarify specification requirements
    send: true
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Pre-Execution Checks

**Check for extension hooks (before specification)**:
- Check if `.specify/extensions.yml` exists in the project root.
- Filter out hooks where `enabled` is explicitly `false`.

## Outline

The text the user typed after `__SPECKIT_COMMAND_SPECIFY__` in the triggering message **is** the feature description.

1. **Generate a concise short name** (2-4 words) for the feature.
2. **Create the spec feature directory** under `specs/<prefix>-<short-name>`.
3. Copy `spec-template` to `SPECIFY_FEATURE_DIRECTORY/spec.md`.
4. Fill spec sections (User Scenarios, Requirements, Success Criteria, Key Entities, Assumptions).
5. **Validate Spec Quality Checklist** at `checklists/requirements.md`.

## Completion Report

Report completion to the user with:
- `SPECIFY_FEATURE_DIRECTORY` — the feature directory path
- `SPEC_FILE` — the spec file path
- Checklist results summary
- **Sugestão de Commit**: Fornecer sugestão de commit Conventional Commits (ex: `docs(spec): add specification for [feature-name]`)
- Readiness for the next phase (`__SPECKIT_COMMAND_CLARIFY__` or `__SPECKIT_COMMAND_PLAN__`)

## Done When

- [ ] Specification written to `SPEC_FILE` and validated against quality checklist
- [ ] Completion reported to user with commit suggestion and next steps
