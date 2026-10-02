# Project Architecture Map: Dotfiles Repository

**Generated Date**: 2026-10-02  
**Repository Root**: `/home/julio/dotfiles`  
**Purpose**: Single authoritative index mapping repo dotfile modules, configuration entrypoints, target system locations, package manifests, installer routines, and privilege boundaries.

---

## 📌 Repository Overview & Architecture

This repository is a modular Linux dotfiles environment designed primarily for **Arch Linux** using **GNU Stow** for user symlink management and a Python-based installation engine (`scripts/installation_script/main.py`).

### Key Technologies & Stack
- **Window Manager**: BSPWM (Binary Space Partitioning Window Manager)
- **Hotkey Daemon**: SXHKD
- **Status Bar**: Polybar
- **Terminal**: Kitty
- **App Launcher**: Rofi
- **Compositor**: Picom
- **File Manager**: Yazi
- **Display Manager**: SDDM (Sugar Candy Theme)
- **Boot Splash**: Plymouth (`umamusume` theme)
- **Deployment Engine**: Python 3 installer (`main.py` + `utils.py`) + GNU Stow

### Ignored / Excluded Modules (`.dotfilesignore`)
The following modules/paths are ignored by repository tools and agent scanners:
- `i3/` (Legacy / alternative i3wm configuration - excluded)
- `gentoo/` (Gentoo Portage / dependencies - excluded)
- Logs (`*.log`, `install.log`), build caches (`__pycache__/`, `.cache/`), archives (`*.7z`, `*.zip`)

---

## 📁 Module & Configuration Index

| Module | Category & Purpose | Repo Entrypoint File | Target System Path | Stow Target |
| :--- | :--- | :--- | :--- | :--- |
| **`bash`** | Shell Configuration | `bash/.bashrc`, `bash/.bash_profile` | `~/.bashrc`, `~/.bash_profile` | `bash` |
| **`bspwm`** | Window Manager | `bspwm/.config/bspwm/bspwmrc` | `~/.config/bspwm/bspwmrc` | `bspwm` |
| **`dirs`** | XDG User Directories | `dirs/.config/user-dirs.dirs` | `~/.config/user-dirs.dirs` | `dirs` |
| **`git`** | Version Control Config | `git/.gitconfig` | `~/.gitconfig` | `git` |
| **`kitty`** | Terminal Emulator | `kitty/.config/kitty/kitty.conf` | `~/.config/kitty/kitty.conf` | `kitty` |
| **`picom`** | Compositor (Effects) | `picom/.config/picom/picom.conf` | `~/.config/picom/picom.conf` | `picom` |
| **`polybar`** | Status Bar | `polybar/.config/polybar/config.ini`, `launch.sh` | `~/.config/polybar/` | `polybar` |
| **`rofi`** | Application Menu | `rofi/.config/rofi/config.rasi` | `~/.config/rofi/config.rasi` | `rofi` |
| **`sddm`** | Display Manager Config | `sddm/etc/sddm.conf.d/theme.conf` | `/etc/sddm.conf.d/theme.conf` | `sddm` (Root Stow) |
| **`sxhkd`** | Hotkey Daemon | `sxhkd/.config/sxhkd/sxhkdrc` | `~/.config/sxhkd/sxhkdrc` | `sxhkd` |
| **`theme`** | GTK / Qt Appearance | `theme/.config/gtk-3.0/`, `qt5ct/`, `qt6ct/` | `~/.config/{gtk-3.0,qt5ct,qt6ct}` | `theme` |
| **`xorg`** | X Server Setup | `xorg/.xinitrc` | `~/.xinitrc` | `xorg` (startx path) |
| **`yazi`** | Terminal File Manager | `yazi/.config/yazi/yazi.toml`, `keymap.toml` | `~/.config/yazi/` | `yazi` |
| **`plymouth`** | Boot Splash Theme | `plymouth/umamusume/` | `/usr/share/plymouth/themes/` | Manual / Unhandled |
| **`wallpapers`** | Desktop Wallpapers | `wallpapers/` (unpacked from `wallpapers.7z`) | `~/dotfiles/wallpapers/` | Asset Extraction |
| **`scripts`** | Helper & Setup Scripts | `scripts/installation_script/main.py`, `utils.py` | `~/dotfiles/scripts/` | Execution Scripts |

---

## 📦 Package & Installer Function Map

| Module | Arch / AUR Packages (`packages.json`) | Installer Function in `utils.py` / `main.py` | Setup Status |
| :--- | :--- | :--- | :--- |
| **`bash`** | `bash-completion` | `apply_stow()` | 🟢 Automated |
| **`bspwm`** | `bspwm` | `apply_stow()` | 🟢 Automated |
| **`dirs`** | `xdg-user-dirs` | `setup_directories()`, `apply_stow()` | 🟢 Automated |
| **`git`** | `git`, `github-cli` | `apply_stow()` | 🟢 Automated |
| **`kitty`** | `kitty` | `apply_stow()` | 🟢 Automated |
| **`picom`** | `picom` | `apply_stow()` | 🟢 Automated |
| **`polybar`** | `polybar` | `apply_stow()` | 🟢 Automated |
| **`rofi`** | `rofi` | `apply_stow()` | 🟢 Automated |
| **`sddm`** | `sddm`, `qt5-graphicaleffects`, `qt5-quickcontrols2`, `qt5-svg` | `setup_sddm()`, `unpack_sddm_theme()`, `apply_sddm_stow()` | 🟡 Interactive (`choice 2`) |
| **`sxhkd`** | `sxhkd` | `apply_stow()` | 🟢 Automated |
| **`theme`** | `gnome-themes-extra`, `qt5ct`, `qt6ct` | `apply_stow()`, `gsettings dark mode` | 🟢 Automated |
| **`xorg`** | `xorg-server`, `xorg-xinit`, `xorg-xrandr`, `xf86-input-libinput` | `setup_startx()` | 🟡 Interactive (`choice 1`) |
| **`yazi`** | `yazi` | `apply_stow()`, `setup_packages()` (`ya pkg install`) | 🟢 Automated |
| **`plymouth`**| Unregistered | None | 🔴 Unhandled |
| **`wallpapers`**| `p7zip` | `unpack_wallpapers()` | 🟢 Automated |

---

## 🔑 Keybinding & Hook Index

### Primary Hotkeys (`sxhkd/.config/sxhkd/sxhkdrc`)
- **Terminal**: `Super + Return` → Launch `kitty`
- **Application Launcher**: `Super + d` → Launch `rofi -show drun`
- **Close Window**: `Super + q` or `Super + k` → `bspc node -c` / `kill`
- **Quit / Reload BSPWM**: `Super + Shift + q` / `Super + Shift + r` → `bspc quit` / `bspc wm -r`
- **Focus Monitor (Multi-Monitor)**: `Super + Tab` / `Super + Shift + Tab` → `scripts/bspwm_focus_monitor.sh`
- **Window State**: `Super + {t, Shift+t, s, f}` → Tiled, Pseudo-tiled, Floating, Fullscreen
- **Volume**: `XF86AudioRaiseVolume` / `LowerVolume` / `Mute` → `pactl set-sink-volume`
- **Brightness**: `Super + Ctrl + Shift + KP_Add / KP_Subtract` → `brightnessctl set`
- **Screenshots**: `Print` (Selection to file), `Print + Shift` (Selection to clipboard), `Ctrl + Shift + s` (Full screen)
- **Random Audio Hook**: `Super + Alt + a` → `scripts/run_random_audio.sh` | `Super + Alt + z` → `pkill mpv`
- **Cheatsheet Windows**: `Super + h` → `bspwm-cheatsheet.py` | `Super + Shift + h` → `reminder_for_commands.py`

### Window Manager Autostart (`bspwm/.config/bspwm/bspwmrc`)
- Starts `sxhkd &`
- Launches Polybar via `$HOME/.config/polybar/launch.sh`
- Starts compositor `picom -b`
- Restores wallpaper / screen layout (`feh` / `xrandr`)
- Launches notification daemon `dunst &`

---

## 🛡️ Privilege & Deployment Boundaries

### 👤 User Space Deployment (`$HOME`)
Managed via **GNU Stow** without root privileges. Targets `.config` and user home files:
- `stow bspwm` → `~/.config/bspwm`
- `stow sxhkd` → `~/.config/sxhkd`
- `stow picom` → `~/.config/picom`
- `stow polybar` → `~/.config/polybar`
- `stow rofi` → `~/.config/rofi`
- `stow kitty` → `~/.config/kitty`
- `stow yazi` → `~/.config/yazi`
- `stow bash` → `~/.bashrc`, `~/.bash_profile`
- `stow git` → `~/.gitconfig`
- `stow theme` → `~/.config/gtk-3.0`, `~/.config/qt5ct`, `~/.config/qt6ct`
- `stow dirs` → `~/.config/user-dirs.dirs`, `~/.config/user-dirs.locale`

### 🔑 Privileged System Space Deployment (`/etc`, `/usr`)
Requires `sudo` elevation during installation:
- **SDDM Configuration**: `sudo stow -t / sddm` → Targets `/etc/sddm.conf.d/theme.conf`
- **SDDM Theme Assets**: `sudo mv sugar-candy /usr/share/sddm/themes/`
- **Pacman Configuration**: `sudo sed` modifications on `/etc/pacman.conf`
- **GRUB Reconfiguration**: `sudo grub-mkconfig -o /boot/grub/grub.cfg`
- **Systemd Services**: `sudo systemctl enable NetworkManager bluetooth ufw sddm`
- **UFW Firewall**: `sudo ufw default deny incoming`, `sudo ufw enable`

---
*Project map generated automatically via `/speckit-map` workflow.*
