---
description: Assess the current codebase against the feature's spec, plan, and tasks, then append any remaining unbuilt work as new tasks to tasks.md so implement can complete it.
handoffs:
  - label: Implement Convergence Tasks
    agent: speckit.implement
    prompt: Start implementation of convergence tasks defined in tasks.md
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

This command evaluates the current codebase against `spec.md`, `plan.md`, and `tasks.md` and appends missing work as tasks.

- **Mandatory Plan Approval**: If convergence findings require major architectural adjustments (e.g., refactoring installer scripts or restructuring dotfile directories), present a Convergence Plan for user approval before appending complex tasks.

## Goal

Close the gap between specified intent and current implementation by appending remaining work to `tasks.md`.

**Modo Dotfiles**: Se `scripts/installation_script/packages.json` existir na raiz do repositório, este comando executa a **Fase 0: Convergência de Componentes Privilegiados** para detectar configs no repo (Plymouth, SDDM, Xorg, etc.) sem rotina no instalador.

## Operating Constraints

**APPEND-ONLY, NEVER REWRITE**: The command's **only** write is appending a new `## Phase N: Convergence` section to `tasks.md`.

## Execution Steps

### Fase 0: Convergência de Componentes Privilegiados (apenas para dotfiles)

1. Carregar contexto do instalador (`packages.json`, `main.py`, `utils.py`).
2. Escanear pastas na raiz do repositório.
3. Classificar gaps (`missing`, `partial`, `contradicts`).
4. Gerar tasks de convergência para pacotes ou rotinas ausentes.

### 1-8. Fases Padrão de Convergência

- Carregar `spec.md`, `plan.md`, `tasks.md`.
- Mapear requisitos não atendidos.
- Se houver trabalho pendente, acrescentar `## Phase N: Convergence` ao final de `tasks.md`.
- Se tudo estiver 100% implementado, manter `tasks.md` inalterado e reportar status de convergência.

## Handoff

Report results and hand off to `__SPECKIT_COMMAND_IMPLEMENT__` to complete the appended convergence tasks.
