---
description: Perform a non-destructive cross-artifact consistency and quality analysis across spec.md, plan.md, and tasks.md after task generation.
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

## Pre-Execution Checks

**Check for extension hooks (before analysis)**:
- Check if `.specify/extensions.yml` exists in the project root.
- If it exists, read it and look for entries under the `hooks.before_analyze` key
- Filter out hooks where `enabled` is explicitly `false`.

## Goal

Identify inconsistencies, duplications, ambiguities, and underspecified items across the three core artifacts (`spec.md`, `plan.md`, `tasks.md`) before implementation. This command MUST run only after `__SPECKIT_COMMAND_TASKS__` has successfully produced a complete `tasks.md`.

## Operating Constraints

**STRICTLY READ-ONLY**: Do **not** modify any files. Output a structured analysis report. Offer an optional remediation plan (user must explicitly approve before any follow-up editing commands would be invoked manually).

**Constitution Authority**: The project constitution (`/memory/constitution.md`) is **non-negotiable** within this analysis scope. Constitution conflicts are automatically CRITICAL.

**Dotfiles Context**: Se o projeto for um repositório de dotfiles (detectado pela presença de `scripts/installation_script/packages.json`), executar adicionalmente a **Fase 0: Auditoria de Coerência do Instalador** antes das fases padrão.

## Execution Steps

### Fase 0: Auditoria de Coerência do Instalador (apenas para dotfiles)

**Executar somente se** `scripts/installation_script/packages.json` ou `packages.json` existir na raiz do repositório.

**Carregar**: `scripts/installation_script/packages.json`, `scripts/installation_script/main.py`, `scripts/installation_script/utils.py`, `.dotfilesignore` / `.agentignore`.

**Verificar as seguintes inconsistências** (gerar findings com prefixo `INS-`):

| Check | Finding ID | Severidade |
|-------|-----------|------------|
| Pasta no repo sem entrada em `stow_packages` | `INS-01` | ALTO |
| Entrada em `stow_packages` sem binário em `packages.json` | `INS-02` | ALTO |
| Pasta com `etc/` ou `usr/` sem função em `utils.py` | `INS-03` | CRÍTICO |
| Função em `utils.py` sem chamada em `main.py` | `INS-04` | CRÍTICO |
| Pacote instalado via hardcode em `utils.py` ausente no `packages.json` | `INS-05` | MÉDIO |
| `__pycache__/`, `*.pyc` ou `install.log` não cobertos pelo `.gitignore` / `.dotfilesignore` | `INS-06` | MÉDIO |

Pastas a excluir da verificação: `.git/`, `.agent/`, `scripts/`, `templates/`, e quaisquer entradas em `.dotfilesignore`.

### 1. Initialize Analysis Context

Run `{SCRIPT}` once from repo root and parse JSON for FEATURE_DIR and AVAILABLE_DOCS. Derive absolute paths:

- SPEC = FEATURE_DIR/spec.md
- PLAN = FEATURE_DIR/plan.md
- TASKS = FEATURE_DIR/tasks.md

### 2. Load Artifacts & Analyze Coverage

Load minimal necessary context from `spec.md`, `plan.md`, `tasks.md`, and `/memory/constitution.md`.

### 3. Build Analysis Report & Next Actions

Output a Markdown report with Findings, Coverage Summary, Constitution Alignment, and Next Actions.
