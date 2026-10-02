---
description: Manage, view, or update ignore rules in .dotfilesignore (or .agentignore) to define which paths the agent must skip.
scripts:
  sh: scripts/bash/resolve-template.sh ignore-template --json
  ps: scripts/powershell/resolve-template.ps1 ignore-template -Json
  py: scripts/python/resolve_template.py ignore-template --json
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Scope Guard

This command manages the `.dotfilesignore` (and fallback `.agentignore`) configuration file.

- You **MUST NOT** remove mandatory security rules (e.g., SSH keys, private tokens, passwords) from the ignore list unless explicitly instructed by the user.

## Outline

You are inspecting or modifying the `.dotfilesignore` file in the project root.

Follow this execution flow:

1. **Check for Ignore File**:
   - Check if `.dotfilesignore` exists in the repository root.
   - If it does not exist, check if `.agentignore` exists.
   - If neither exists, copy `templates/ignore-template.md` to `.dotfilesignore` as the default ignore file.

2. **Process User Request**:
   - **Add Rules**: If `$ARGUMENTS` contains new paths or glob patterns (e.g., `add sddm_theme.7z` or `ignore *.bak`), append them under the appropriate section in `.dotfilesignore` without creating duplicate entries.
   - **Check Path**: If `$ARGUMENTS` asks to check a specific path (e.g., `check wallpapers.7z`), evaluate whether git wildmatch / fnmatch rules in `.dotfilesignore` match that path and report the result.
   - **View Rules**: If `$ARGUMENTS` is empty or asks to list/view, output the current formatted contents of `.dotfilesignore`.

3. **Validate Exclusions**:
   - Confirm that sensitive credential patterns (`id_rsa`, `*.pem`, `*.key`, `.ssh/`, `.gnupg/`) remain protected.

4. **Completion Report & Commit Suggestion**:
   - Save changes to `.dotfilesignore`.
   - Provide a concise summary of active ignore rules or modifications made.
   - **Sugestão de Commit**: Fornecer sugestão de commit Conventional Commits (ex: `chore(ignore): update .dotfilesignore rules`).
