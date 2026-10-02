---
description: Analyze whether the installation scripts and package manifests are coherent and synchronized with the repository dotfiles.
handoffs:
  - label: Implement Audit Fix Tasks
    agent: speckit.implement
    prompt: Implement installation audit fix tasks defined in tasks.md
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

This command performs an audit comparing repository dotfile modules against installation scripts and generates remediation tasks.

- **Mandatory Plan Approval**: You **MUST NOT** modify installation scripts (`main.py`, `utils.py`, `packages.json`) without presenting an explicit Remediation Plan and obtaining user approval.

## Outline

You are auditing the repository's installation script and package manifests against the actual dotfiles folders.

Follow this execution flow:

1. **Discover Dotfiles Modules & Installer Scripts**:
   - List all top-level directories in the repository (excluding `.git`, `.agent`, `templates`, `.specify`, `specs`, and paths ignored by `.dotfilesignore`).
   - Locate package definition files (`scripts/installation_script/packages.json`) and installer scripts (`main.py`, `utils.py`, `install.sh`).

2. **Cross-Check Analysis**:
   - **Package Mirroring**: Check if every dotfile module has its base package listed in `packages.json`.
   - **Installer Routines**: Check if every privileged config (`/etc/`, `/usr/share/`) has an explicit setup function in `utils.py` and call in `main.py`.
   - **Stow Isolation & Idempotency**: Verify user vs root separation and check continuous re-execution safety.

3. **Generate Coherence Report & Remediation Plan**:
   - Save report to `.specify/reports/install-audit.md` with:
     - 🟢 **Compliant Modules**
     - 🟡 **Warnings**
     - 🔴 **Critical Gaps**
     - **Proposed Remediation Plan**

4. **Task Generation & Append Protocol**:
   - If user approves fixing the identified gaps:
     - Check if `tasks.md` exists in the active feature directory or root.
     - Append a new section: `## Phase N: Installation Audit Fixes`.
     - Add checklist items in the format:
       `- [ ] T### [P?] [Audit] Add package [pkg] to packages.json`
       `- [ ] T### [P?] [Audit] Implement setup_[module]() in scripts/installation_script/utils.py`
       `- [ ] T### [Audit] Call setup_[module]() in scripts/installation_script/main.py`

5. **Completion Report & Commit Suggestion**:
   - Present report and tasks summary.
   - **Sugestão de Commit**: Fornecer sugestão de commit Conventional Commits (ex: `chore(audit): audit installation scripts and package coherence`).
   - Hand off to `__SPECKIT_COMMAND_IMPLEMENT__` to execute the audit fix tasks.
