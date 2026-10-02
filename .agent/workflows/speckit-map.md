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
   - Locate main configuration files within each module (e.g., `kitty/.config/kitty/kitty.conf`, `bspwm/.config/bspwm/bspwmrc`, `sxhkd/.config/sxhkd/sxhkdrc`).
   - Record target installation locations (`$HOME/.config/...`, `/etc/...`, `/usr/share/...`).

3. **Map Packages and Installer Routines**:
   - Cross-reference each module with `scripts/installation_script/packages.json` to list required packages (pacman / AUR / distro native).
   - Cross-reference each module with `scripts/installation_script/utils.py` and `main.py` to index the python setup functions (e.g., `setup_plymouth()`, `setup_sddm()`).

4. **Generate `.specify/memory/project-map.md`**:
   - Create directory `.specify/memory` if it does not exist.
   - Format the project map with clear sections:
     - 📌 **Repository Overview & Architecture**
     - 📁 **Module & Configuration Index** (Module → Entrypoint → Target System Path)
     - 📦 **Package & Installer Function Map** (Module → Base Package → Setup Routine in `utils.py`)
     - 🔑 **Keybinding & Hook Index** (Hotkeys in `sxhkdrc`, systemd units, Xorg configs)
     - 🛡️ **Privilege & Deployment Boundaries** (User Stow modules vs. Root Sudo modules)

5. Save the file to `.specify/memory/project-map.md` and display a summary of indexed modules to the user.
