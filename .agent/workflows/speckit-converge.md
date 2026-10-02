---
description: Assess the current codebase against the feature's spec, plan, and tasks, then append any remaining unbuilt work as new tasks to tasks.md so implement can complete it.
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

**Check for extension hooks (before convergence)**:
- Check if `.specify/extensions.yml` exists in the project root.
- Filter out hooks where `enabled` is explicitly `false`.

## Goal

Close the gap between what a feature's specification, plan, and tasks call for and what the repository currently implements. Read `spec.md`, `plan.md`, and `tasks.md` as the **sole source of intent** (with the constitution as governing constraints), assess the current state of the repo, and **append remaining work as new tasks** at the bottom of `tasks.md` so that `__SPECKIT_COMMAND_IMPLEMENT__` can complete it.

**Modo Dotfiles**: Se scripts de instalação (`scripts/installation_script/packages.json`) existirem na raiz do repositório, este comando executa a **Fase 0: Convergência de Componentes Privilegiados** para verificar se todas as pastas de dotfiles têm suporte correspondente nos scripts de instalação.

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

## Done When

- [ ] Repository assessed against spec, plan, and tasks
- [ ] Any remaining unbuilt work appended to tasks.md as a new Phase N: Convergence
- [ ] Completion reported to user
