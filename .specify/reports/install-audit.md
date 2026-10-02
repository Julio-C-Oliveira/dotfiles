# Coherence Audit Report: Dotfiles & Installer Scripts

**Date**: 2026-10-02  
**Target Repository**: `/home/julio/dotfiles`  
**Audit Scope**: Consistency between active top-level dotfile modules (respecting `.dotfilesignore`), package manifests (`scripts/installation_script/packages.json`), and setup routines (`scripts/installation_script/main.py`, `utils.py`).

---

## 1. Executive Summary

An updated audit was performed following the exclusion of `i3/` and `gentoo/` in `.dotfilesignore`. Scanning the repository's active modules against `packages.json` and `main.py` shows that all active user-space desktop modules (`bspwm`, `polybar`, `picom`, `kitty`, `rofi`, `yazi`, `sxhkd`, `bash`, `git`, `theme`, `dirs`) are **100% compliant** and correctly mapped to GNU Stow targets.

However, **one critical gap** remains regarding system splash screen configuration (`plymouth`), along with minor warnings around interactive script execution and hardcoded paths.

---

## 2. Coherence Status

### 🟢 Compliant Modules (11 Active Modules)
These active dotfile modules are correctly mapped in `stow_packages` in `packages.json` and have their corresponding packages registered in `arch_packages` or `yay_packages`:

| Module | Target Path(s) | Package(s) Registered | Installer Handler |
| :--- | :--- | :--- | :--- |
| **`bash`** | `.bashrc`, `.bash_profile` | `bash-completion` | `apply_stow()` |
| **`bspwm`** | `.config/bspwm` | `bspwm` | `apply_stow()` |
| **`dirs`** | `.config/user-dirs.dirs`, `.config/user-dirs.locale` | `xdg-user-dirs` | `apply_stow()` + `setup_directories()` |
| **`git`** | `.gitconfig` | `git`, `github-cli` | `apply_stow()` |
| **`kitty`** | `.config/kitty` | `kitty` | `apply_stow()` |
| **`picom`** | `.config/picom` | `picom` | `apply_stow()` |
| **`polybar`** | `.config/polybar` | `polybar` | `apply_stow()` |
| **`rofi`** | `.config/rofi` | `rofi` | `apply_stow()` |
| **`sxhkd`** | `.config/sxhkd` | `sxhkd` | `apply_stow()` |
| **`theme`** | `.config/gtk-3.0`, `.config/qt5ct`, `.config/qt6ct`, `.config/QtProject.conf` | `gnome-themes-extra`, `qt5ct`, `qt6ct` | `apply_stow()` + `gsettings dark mode` |
| **`yazi`** | `.config/yazi` | `yazi` | `apply_stow()` + `ya pkg install` |

---

### ⚪ Excluded / Ignored Modules (`.dotfilesignore`)
The following top-level directories are intentionally excluded from installer auditing via `.dotfilesignore`:
- **`i3/`**: Alternative window manager configuration (Ignored).
- **`gentoo/`**: Distro-specific portage configuration (Ignored).

---

### 🟡 Warnings & Minor Inconsistencies (5 Items)

1. **`xorg` Module Path Scope**:
   - `xorg/.xinitrc` is not listed in `stow_packages` in `packages.json`. It is only stowed conditionally inside `setup_gui()` if choice `[1]` (`startx`) is selected.
2. **Interactive `input()` Invocations**:
   - `setup_gui()` in `utils.py:338` blocks execution with `input("[1] - startx\n[2] - sddm\nchoice: ")`.
   - `main.py:98` prompts interactively for system reboot (`input("Deseja reiniciar o sistema agora?...")`).
   - *Impact*: Prevents non-interactive / unattended automated setup.
3. **Hardcoded Repository Path Assumptions**:
   - `utils.py` uses `Path.home() / "dotfiles"` across multiple functions (`apply_stow`, `apply_sddm_stow`, `unpack_wallpapers`, `unpack_sddm_theme`). If the repository is cloned elsewhere, the installer fails.
4. **Destructive Conflict Resolution in `apply_stow`**:
   - `utils.py:202-207` uses `shutil.rmtree(target_path)` / `unlink()` to clear existing target paths before `stow`. Pre-existing uncommitted files in `~/.config/bspwm` would be erased without backup.
5. **AUR `yay` Clone Directory Collisions**:
   - `utils.py:157` clones `yay` to `/tmp/yay`. If `/tmp/yay` already exists from a previous interrupted run, `git clone` fails.

---

### 🔴 Critical Gaps (1 Module)

1. **`plymouth` System Module Unhandled**:
   - **Repository Path**: `plymouth/umamusume/` (Boot splash screen theme present in active modules).
   - **Issue**: There is **no package entry** for `plymouth` in `packages.json` and **no Python function** in `utils.py` or `main.py` to copy `plymouth/umamusume` to `/usr/share/plymouth/themes/` or set the active theme via `plymouth-set-default-theme`.
   - **Result**: Boot animation theme remains unconfigured during automated setup.

---

## 3. Actionable Recommendations

1. **Implement Plymouth Setup Routine**:
   - Add `plymouth` package to `packages.json`.
   - Implement `setup_plymouth()` in `utils.py` to copy `plymouth/umamusume` to `/usr/share/plymouth/themes/umamusume` and configure Plymouth.

2. **Add CLI Arguments for Unattended Execution**:
   - Support command-line flags (e.g., `--gui sddm|startx`, `--no-reboot`) to bypass interactive `input()` prompts.

3. **Dynamic Path Resolution & Safe Stow Backups**:
   - Dynamically detect repository root directory relative to script execution location.
   - Implement timestamped backup directories (`.bak`) before unlinking pre-existing target files in `apply_stow()`.

---
*Report generated automatically via `/speckit-audit-install` workflow.*
