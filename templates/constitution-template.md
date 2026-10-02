# [PROJECT_NAME] Constitution
<!-- Example: Dotfiles System Governance, Arch/Gentoo Workstation Constitution, etc. -->

## Core Principles

### [PRINCIPLE_1_NAME]
<!-- Example: I. Package Mirroring (Mandatory) -->
[PRINCIPLE_1_DESCRIPTION]
<!-- Example: No application configuration may be added to the repository without its base package registered in the package manager list and supported by the installation script. -->

### [PRINCIPLE_2_NAME]
<!-- Example: II. Complete Installer Routine -->
[PRINCIPLE_2_DESCRIPTION]
<!-- Example: Every privileged configuration (/etc/, /usr/share/, system hooks) MUST have an explicit, automated setup routine in the installation script. -->

### [PRINCIPLE_3_NAME]
<!-- Example: III. User/Root Isolation & Symlinks -->
[PRINCIPLE_3_DESCRIPTION]
<!-- Example: User configurations are managed exclusively via GNU Stow/symlinks. Privileged configurations belong strictly in the installation script with explicit sudo elevation. NEVER mix. -->

### [PRINCIPLE_4_NAME]
<!-- Example: IV. Idempotency -->
[PRINCIPLE_4_DESCRIPTION]
<!-- Example: All installer scripts and setup functions MUST be safe for continuous re-execution (e.g. check existence before copying/linking, use package flags like --needed). -->

### [PRINCIPLE_5_NAME]
<!-- Example: V. Secrets Safety (NON-NEGOTIABLE) -->
[PRINCIPLE_5_DESCRIPTION]
<!-- Example: Versioning SSH private keys, API tokens, passwords or sensitive credentials is strictly prohibited. Use sops/pass/gpg or local secret stores. -->

### [PRINCIPLE_6_NAME]
<!-- Example: VI. Repository Hygiene & Ignore Policy -->
[PRINCIPLE_6_DESCRIPTION]
<!-- Example: Keep build caches, logs, and temporary user state out of git. Respect .dotfilesignore at all times. Binaries and large archives must be evaluated for Git LFS or external download. -->

## [SECTION_2_NAME]
<!-- Example: System Architecture & Platform Support -->

[SECTION_2_CONTENT]
<!-- Example: Target Linux distribution(s), desktop environments, shell standards, package managers, deployment policies, etc. -->

## [SECTION_3_NAME]
<!-- Example: Installation Workflow & Maintenance -->

[SECTION_3_CONTENT]
<!-- Example: Dry-run testing requirements, automated setup scripts, symlink validation gates, etc. -->

## Governance
<!-- Example: Constitution supersedes all other practices; Amendments require documentation, approval, migration plan -->

[GOVERNANCE_RULES]
<!-- Example: All PRs/commits must verify compliance with installation scripts and .dotfilesignore; Complexity must be justified; Version bumps strictly enforced -->

**Version**: [CONSTITUTION_VERSION] | **Ratified**: [RATIFICATION_DATE] | **Last Amended**: [LAST_AMENDED_DATE]
<!-- Example: Version: 1.0.0 | Ratified: 2026-10-02 | Last Amended: 2026-10-02 -->
