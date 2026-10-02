---
description: Analyze whether the installation scripts and package manifests are coherent and synchronized with the repository dotfiles.
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

This command performs a non-destructive analysis and generates an audit report regarding the coherence between repository dotfile modules and installation scripts.

- You **MUST NOT** modify installation scripts or dotfiles during this analysis phase.
- If requested to fix gaps, extract those tasks into follow-up implementation intents (`speckit-tasks` or `speckit-implement`).

## Outline

You are auditing the repository's installation script and package manifests against the actual dotfiles folders.

Follow this execution flow:

1. **Discover Dotfiles Modules**:
   - List all top-level directories in the repository (excluding `.git`, `.agent`, `templates`, `.specify`, `specs`, and paths ignored by `.dotfilesignore`).
   - Identify modules representing user configurations (e.g., `kitty`, `bspwm`, `polybar`, `rofi`, `yazi`, `i3`, `picom`, `bash`, `git`, etc.) and system/root configurations (e.g., `plymouth`, `sddm`, `xorg`, `gentoo`).

2. **Discover Installer Manifests & Scripts**:
   - Locate package definition files (e.g., `scripts/installation_script/packages.json`, `packages.txt`, `Brewfile`).
   - Locate installer logic scripts (e.g., `scripts/installation_script/main.py`, `utils.py`, `install.sh`, `setup.sh`).

3. **Cross-Check Analysis**:
   - **Package Mirroring**: Check if every dotfile module has its corresponding package listed in the package manifest (`packages.json` or equivalent). Report any dotfile module that lacks a registered package.
   - **Installer Routines**: Check if every system/privileged configuration (e.g., SDDM themes, Plymouth configs, Xorg configs, etc.) has an explicit installation function/call in the setup scripts.
   - **Stow vs. Root Separation**: Verify that user configs are set up via GNU Stow / user symlinks and system configs are handled via installer scripts with proper `sudo` elevation.
   - **Idempotency Audit**: Inspect installer script logic to confirm operations use safe re-execution patterns (e.g., `--needed` for pacman, existence checks before file copying, `shutil.which()`).

4. **Generate Coherence Report**:
   - Write or display an audit summary containing:
     - 🟢 **Compliant Modules**: Dotfiles correctly mapped to packages and installer routines.
     - 🟡 **Warnings**: Optional packages missing, unused package entries, or minor path inconsistencies.
     - 🔴 **Critical Gaps**: Dotfile modules present in the repo with NO corresponding package or installer routine.
     - **Actionable Recommendations**: List of tasks needed to bring installation scripts to 100% coherence.

5. Save the report to `.specify/reports/install-audit.md` and present the key findings to the user.
