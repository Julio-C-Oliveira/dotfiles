---
description: Analyze external changes in the local system (~/.config, /etc, etc.) that differ from or are missing in the dotfiles repository.
handoffs:
  - label: Implement Drift Sync Tasks
    agent: speckit.implement
    prompt: Implement drift synchronization tasks defined in tasks.md
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

## Scope Guard & Plan-First Gate

This command performs analysis comparing the host system's live configuration files against the dotfiles repository and generates sync tasks.

- **Mandatory Plan Approval**: You **MUST NOT** copy, overwrite, or import system files into the repository without presenting an explicit Sync Plan and obtaining user approval.
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

4. **Produce Drift Analysis & Import Plan**:
   - Write or display a summary report in `.specify/reports/drift-analysis.md` containing:
     - 📝 **Modified Files**: Files in repo that have local changes.
     - 🆕 **Import Candidates**: Untracked configurations in `$HOME/.config` eligible to become new dotfiles modules.
     - ⚠️ **Missing / Broken Symlinks**: Repo configs that are not properly linked in the live system.
     - 🛡️ **Ignored Items**: Summary of paths skipped per `.dotfilesignore`.

5. **Task Generation & Append Protocol**:
   - If user approves importing/synchronizing the detected drift:
     - Check if `tasks.md` exists in the active feature directory or root.
     - Append a new section: `## Phase N: System Drift Sync Tasks`.
     - Add checklist items in the format:
       `- [ ] T### [P?] [Drift] Copy ~/.config/[app] to [app]/.config/[app]`
       `- [ ] T### [P?] [Drift] Register [app] package in packages.json`
       `- [ ] T### [P?] [Drift] Execute stow -R [app]`

6. **Completion Report & Commit Suggestion**:
   - Report generated plan and tasks summary.
   - **Sugestão de Commit**: Fornecer sugestão de commit Conventional Commits (ex: `chore(drift): detect and stage local system configuration drift`).
   - Hand off to `__SPECKIT_COMMAND_IMPLEMENT__` to execute the sync tasks safely.
