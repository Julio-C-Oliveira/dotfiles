---
description: Generate an actionable, dependency-ordered tasks.md for the feature based on available design artifacts.
handoffs:
  - label: Analyze For Consistency
    agent: speckit.analyze
    prompt: Run a project analysis for consistency
    send: true
  - label: Implement Project
    agent: speckit.implement
    prompt: Start the implementation in phases
    send: true
scripts:
  sh: scripts/bash/setup-tasks.sh --json
  ps: scripts/powershell/setup-tasks.ps1 -Json
  py: scripts/python/setup_tasks.py --json
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Pre-Execution Checks

**Check for extension hooks (before tasks generation)**:
- Check if `.specify/extensions.yml` exists in the project root.
- Filter out hooks where `enabled` is explicitly `false`.

## Outline

1. **Setup**: Run `{SCRIPT}` from repo root and parse JSON.
2. **Load design documents**: Read `plan.md`, `spec.md`, `research.md`, `/memory/constitution.md`, `.specify/memory/project-map.md`.
3. **Execute task generation workflow**:
   - Generate tasks organized by scenario/module.
   - Format each task: `- [ ] [TaskID] [P?] [Scenario] Description with exact file path`.

## Completion Report

Output path to generated tasks.md and summary:
- Total task count and scenario breakdown.
- Parallel opportunities identified.
- **Sugestão de Commit**: Fornecer sugestão de commit Conventional Commits (ex: `docs(tasks): generate implementation task list for [feature-name]`).

## Done When

- [ ] tasks.md generated with all phases, task IDs, and file paths
- [ ] Completion reported to user with commit suggestion
