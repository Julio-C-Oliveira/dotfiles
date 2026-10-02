---

description: "Task list template for dotfiles and system module implementation"
---

# Tasks: [FEATURE / MODULE NAME]

**Input**: Design documents from `/specs/[###-feature-name]/`

**Prerequisites**: plan.md (required), spec.md (required for scenarios), research.md

**Organization**: Tasks are grouped by system module / scenario to enable independent implementation and testing.

## Format: `[ID] [P?] [Scenario] Description`

- **[P]**: Can run in parallel (different files/modules, no dependencies)
- **[Scenario]**: Which scenario/module this task belongs to (e.g., S1, S2, S3)
- Include exact file paths in descriptions

## Path Conventions

- **Modular Dotfiles**: `[module]/`, e.g., `kitty/`, `bspwm/`, `zsh/`
- **Installation Scripts**: `scripts/installation_script/`, `scripts/utils/`
- **Root Configurations**: `etc/` or installer handlers

---

## Phase 1: Setup & Directory Structure

**Purpose**: Module directory creation and base files initialization

- [ ] T001 Create module directory structure in `[module_name]/`
- [ ] T002 Initialize configuration file scaffold in `[module_name]/.config/[module]/`
- [ ] T003 [P] Verify path alignment with GNU Stow or installation manager

---

## Phase 2: Package Registration & Installer Integration

**Purpose**: Ensure dependencies and install routines exist before deploying configs

- [ ] T004 Register required packages in `scripts/installation_script/packages.json` (or distro package list)
- [ ] T005 [P] Add setup routine / handler in installer script (`main.py` / `utils.py` / `install.sh`)
- [ ] T006 [P] Verify installer idempotency (check existence, `--needed` flags, non-destructive file operations)

---

## Phase 3: Scenario 1 - [Title] (Priority: P1) 🎯 MVP

**Goal**: [Brief description of what this scenario/module delivers]

**Independent Test**: [How to verify this scenario works on its own, e.g. `stow -n -v [module]` or dry-run script]

### Implementation for Scenario 1

- [ ] T007 [P] [S1] Create/update main configuration file in `[module]/.config/[app]/[config_file]`
- [ ] T008 [P] [S1] Configure keybindings / themes / options in `[module]/.config/[app]/[theme_file]`
- [ ] T009 [S1] Add helper scripts or hooks in `scripts/` or `[module]/bin/`
- [ ] T010 [S1] Update installer logic to link or copy module files

**Checkpoint**: At this point, Scenario 1 should be fully functional and deployable independently

---

## Phase 4: Scenario 2 - [Title] (Priority: P2)

**Goal**: [Brief description of what this scenario delivers]

**Independent Test**: [How to verify this scenario works on its own]

### Implementation for Scenario 2

- [ ] T011 [P] [S2] Create/update configuration file in `[module]/.config/[app]/[config_file]`
- [ ] T012 [S2] Add environment variables or shell alias in `bash/` / `zsh/`
- [ ] T013 [S2] Integrate with Scenario 1 components (if needed)

**Checkpoint**: At this point, Scenarios 1 AND 2 should both work independently

---

## Phase N: Verification, Hygiene & Security Audit

**Purpose**: Validate dotfile integrity and security compliance

- [ ] TXXX [P] Verify no secrets, private keys, or credentials exist in new configuration files
- [ ] TXXX Check `.dotfilesignore` to ensure build caches or temporary files are excluded
- [ ] TXXX Run dry-run installation test (`stow -n -v` or installer test mode)
- [ ] TXXX Perform `speckit-audit-install` to ensure 100% coherence between dotfiles and installer
