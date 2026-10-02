---
description: Generate or update a comprehensive architectural project map (.specify/memory/project-map.md) indexing all dotfile modules, installer routines, and system entrypoints to minimize context loading.
scripts:
  sh: scripts/bash/resolve-template.sh spec-template --json
  ps: scripts/powershell/resolve-template.ps1 spec-template -Json
  py: scripts/python/resolve_template.py spec-template --json
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Scope Guard

This command scans the project structure and generates/updates a token-efficient Project Map index at `.specify/memory/project-map.md`.

- You **MUST NOT** modify any application configurations or installation scripts during this mapping phase.
- You **MUST** respect `.dotfilesignore` / `.agentignore` to skip build caches and sensitive keys.

## Outline

You are indexing the dotfiles repository to create a single authoritative reference map.

Follow this execution flow:

1. **Scan Repository Modules**:
   - List all directories in the repository (excluding `.git`, `.agent`, `templates`, `.specify`, `specs`, and paths matching `.dotfilesignore`).
   - Identify module purpose (e.g. `kitty` → Terminal, `bspwm` → Window Manager, `sxhkd` → Hotkey Daemon, `polybar` → Status Bar, `yazi` → File Manager, `plymouth` → Boot Splash, `sddm` → Display Manager).

2. **Index Configuration Entrypoints**:
   - Locate main configuration files within each module.
   - Record target installation locations.

3. **Map Packages and Installer Routines**:
   - Cross-reference each module with `packages.json`, `utils.py`, `main.py`.

4. **Generate `.specify/memory/project-map.md`**:
   - Create directory `.specify/memory` if missing.
   - Format module index, package map, keybinding index, privilege boundaries.

5. **Completion Report & Commit Suggestion**:
   - Save `.specify/memory/project-map.md` and summary.
   - **Sugestão de Commit**: Fornecer sugestão de commit Conventional Commits (ex: `docs(map): update project architecture map (.specify/memory/project-map.md)`).
