---
description: Analyze external changes in the local system (~/.config, /etc, etc.) that differ from or are missing in the dotfiles repository.
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

This command performs a non-destructive analysis comparing the host system's live configuration files against the dotfiles repository.

- You **MUST NOT** automatically copy or overwrite system files or repository files without explicit user approval.
- You **MUST** strictly respect rules defined in `.dotfilesignore` (or `.agentignore`) to avoid reading private keys or sensitive system caches.

## Outline

You are scanning the local system to detect drift and unimported configurations.

Follow this execution flow:

1. **Load Ignore Rules**:
   - Read `.dotfilesignore` (and `.agentignore` if present). Ensure patterns like `id_rsa`, `__pycache__`, `.cache`, `*.key`, `*.pem`, `*.log`, `install.log` are filtered out.

2. **Scan Active System Paths**:
   - Inspect `$HOME/.config` and key shell files (`.bashrc`, `.zshrc`, `.xprofile`, `.Xresources`, etc.).
   - If user input specifies target directories (e.g. `/etc/sddm.conf.d`, `/etc/X11/xorg.conf.d`), include those paths.

3. **Compare Against Repository**:
   - For each module in the dotfiles repo:
     - Compare file content between repository version and active system version.
     - Detect **Modified Content** (repo file differs from live file).
   - For untracked directories in `$HOME/.config`:
     - Detect **New Un-imported Applications** (e.g. user installed a new tool `fastfetch` and configured it in `~/.config/fastfetch`, but it is not in the repo).

4. **Produce Drift Analysis Report**:
   - Write or display a summary report containing:
     - 📝 **Modified Files**: Files in repo that have local changes.
     - 🆕 **Import Candidates**: Untracked configurations in `$HOME/.config` eligible to become new dotfiles modules.
     - ⚠️ **Missing / Broken Symlinks**: Repo configs that are not properly linked in the live system.
     - 🛡️ **Ignored Items**: Summary of paths skipped per `.dotfilesignore`.
   - Provide explicit import instructions (e.g. `cp -r ~/.config/[app] [app]/.config/` or Stow commands).

5. Save the report to `.specify/reports/drift-analysis.md` and present key findings to the user.
