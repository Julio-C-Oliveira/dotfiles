# Coherence Audit Report: Dotfiles & Installer Scripts

**Date**: 2026-10-02  
**Target Repository**: `/home/julio/dotfiles`  
**Audit Scope**: Consistency between top-level dotfile modules, package manifests (`scripts/installation_script/packages.json`), and setup routines (`scripts/installation_script/main.py`, `utils.py`).

---

## 1. Executive Summary

An audit of the repository's modules against the Python installer script (`main.py` & `utils.py`) and package definition (`packages.json`) revealed that while the core Arch Linux desktop environment (`bspwm`, `polybar`, `picom`, `kitty`, `rofi`, etc.) is well-integrated with GNU Stow, there are **critical gaps** regarding missing Stow targets (`i3`), unhandled system configurations (`plymouth`, `gentoo`), interactive blocking calls in automated setup routines, and destructive cleanups in `apply_stow`.

---

## 2. Coherence Status

### 🟢 Compliant Modules (11 Modules)
These dotfile modules are correctly mapped in `stow_packages` in `packages.json` and have their corresponding packages registered in `arch_packages` or `yay_packages`:

| Module | Target Path(s) | Package(s) Registered | Installer Handler |
| :--- | :--- | :--- | :--- |
| **`bash`** | `.bashrc`, `.bash_profile` | `bash-completion` | `apply_stow` |
| **`bspwm`** | `.config/bspwm` | `bspwm` | `apply_stow` |
| **`dirs`** | `.config/user-dirs.dirs`, `.config/user-dirs.locale` | `xdg-user-dirs` | `apply_stow` + `setup_directories` |
| **`git`** | `.gitconfig` | `git`, `github-cli` | `apply_stow` |
| **`kitty`** | `.config/kitty` | `kitty` | `apply_stow` |
| **`picom`** | `.config/picom` | `picom` | `apply_stow` |
| **`polybar`** | `.config/polybar` | `polybar` | `apply_stow` |
| **`rofi`** | `.config/rofi` | `rofi` | `apply_stow` |
| **`sxhkd`** | `.config/sxhkd` | `sxhkd` | `apply_stow` |
| **`theme`** | `.config/gtk-3.0`, `.config/qt5ct`, `.config/qt6ct`, `.config/QtProject.conf` | `gnome-themes-extra`, `qt5ct`, `qt6ct` | `apply_stow` + `gsettings dark mode` |
| **`yazi`** | `.config/yazi` | `yazi` | `apply_stow` + `ya pkg install` |

---

### 🟡 Warnings & Minor Inconsistencies (5 Items)

1. **`xorg` Module Path Scope**:
   - `xorg/.xinitrc` is not in `stow_packages`. It is only stowed conditionally inside `setup_gui()` if the user selects choice `[1] (startx)`. If the user selects SDDM or runs headless, `.xinitrc` is never deployed.
2. **Interactive `input()` Invocations in `main.py` / `utils.py`**:
   - `setup_gui()` in `utils.py:338` blocks execution with `input("[1] - startx\n[2] - sddm\nchoice: ")`.
   - `main.py:98` prompts interactively for system reboot (`input("Deseja reiniciar o sistema agora?...")`).
   - *Impact*: Prevents non-interactive unattended installation.
3. **Hardcoded Repository Path Assumptions**:
   - `utils.py` uses `Path.home() / "dotfiles"` in multiple functions (`apply_stow`, `apply_sddm_stow`, `unpack_wallpapers`, `unpack_sddm_theme`). If the repository is cloned to a different path (e.g. `~/projects/dotfiles`), the installer breaks.
4. **Destructive Conflict Resolution in `apply_stow`**:
   - `utils.py:202-207` uses `shutil.rmtree(target_path)` / `unlink()` to remove target paths before running `stow`. If a user has pre-existing uncommitted local files in `~/.config/bspwm`, they will be permanently lost without backup.
5. **AUR `yay` Clone Directory Collisions**:
   - `utils.py:157` clones `yay` to `/tmp/yay`. If `/tmp/yay` already exists from a previous interrupted run, `git clone` will fail.

---

### 🔴 Critical Gaps (3 Modules)

1. **`i3` Module Missing from `packages.json`**:
   - **Repository Path**: `i3/.config/i3/config` (8.3 KB configuration file present).
   - **Issue**: `i3` is **NOT** registered in `stow_packages` in `packages.json`, nor is `i3-wm` listed in `arch_packages`.
   - **Result**: The `i3` window manager config in this repository is completely ignored during installation.

2. **`plymouth` System Module Unhandled**:
   - **Repository Path**: `plymouth/umamusume/` (Plymouth splash screen theme).
   - **Issue**: There is **no package entry** for `plymouth` in `packages.json` and **no Python function** in `utils.py` or `main.py` to copy/symlink `plymouth/umamusume` to `/usr/share/plymouth/themes/` or run `plymouth-set-default-theme`.
   - **Result**: Boot animation configurations are left unconfigured.

3. **`gentoo` Distro Configuration Decoupled**:
   - **Repository Path**: `gentoo/make.conf`, `gentoo/install_dependencies`, `gentoo/dependencies.txt`.
   - **Issue**: The installer framework exclusively targets Arch Linux (`pacman`, `yay`, `grub-mkconfig`). Gentoo package manifests and portage configurations are not recognized or modularized by `main.py`.

---

## 3. Actionable Recommendations

To achieve 100% coherence and robust installation automation, the following tasks are recommended:

1. **Fix Missing Stow Packages (`i3`)**:
   - Add `i3-wm` (or `i3-gaps`) to `arch_packages` in `packages.json`.
   - Add `{"name": "i3", "target": [".config/i3"]}` to `stow_packages` in `packages.json`.

2. **Implement Plymouth Setup Routine**:
   - Add `plymouth` to `arch_packages` in `packages.json`.
   - Add a function `setup_plymouth()` in `utils.py` to copy `plymouth/umamusume` to `/usr/share/plymouth/themes/umamusume` and set the active theme.

3. **Refactor Hardcoded Repo Paths & Destructive Cleanup**:
   - Dynamic repository root detection: Determine repo root relative to `__file__` or via `git rev-parse --show-toplevel` instead of hardcoding `~/dotfiles`.
   - Safe backup before stow: Create timestamped backups (`.bak`) before unlinking target paths instead of using `shutil.rmtree()`.

4. **Add CLI Flags for Non-Interactive Execution**:
   - Add command-line arguments to `main.py` (e.g., `--gui=sddm|startx`, `--no-reboot`, `--yes`) to bypass interactive `input()` prompts.

5. **Multi-Distro Abstraction**:
   - Structure `packages.json` or distro submodules so system-specific setups (Arch vs Gentoo) can be selected via configuration or system detection.

---
*Report generated automatically via `/speckit-audit-install` workflow.*
