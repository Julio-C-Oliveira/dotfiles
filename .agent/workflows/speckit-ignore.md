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
   - **Add Rules**: If `$ARGUMENTS` contains new paths or glob patterns, append them to `.dotfilesignore`.
   - **Check Path**: Evaluate path against `.dotfilesignore` rules.
   - **View Rules**: Output current contents of `.dotfilesignore`.

3. **Validate Exclusions**:
   - Confirm sensitive patterns (`id_rsa`, `*.pem`, `*.key`, `.ssh/`, `.gnupg/`) remain protected.

4. **Completion Report & Commit Suggestion**:
   - Save changes to `.dotfilesignore`.
   - Provide summary of active ignore rules or modifications made.
   - **Sugestão de Commit**: Fornecer sugestão de commit Conventional Commits (ex: `chore(ignore): update .dotfilesignore rules`).
