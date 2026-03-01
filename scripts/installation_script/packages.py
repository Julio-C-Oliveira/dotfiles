arch_packages = [
    # Display server:
    "xorg-server", "xorg-xinit", "xorg-xrandr", "xf86-input-libinput", "xdg-user-dirs",

    # Drivers:
    "brightnessctl", "network-manager-applet", "networkmanager",

    # Audio:
    "pipewire", "pipewire-pulse", "pipewire-alsa", "wireplumber", "pavucontrol",

    # Bluetooth:
    "bluez", "bluez-utils", "blueman",

    # Segurança:
    "ufw",

    # Window Manger e Relacionados:
    "bspwm", "sxhkd", 
    "picom", "polybar", "rofi",

    # Sistema e integrações:
    "polkit-gnome", "xdg-utils", "bash-completion", "xclip",

    # Gerenciamento de arquivos:
    "gvfs", "gvfs-mtp", "gvfs-smb",

    # Ferramentas:
    "base-devel", "git", "stow", "vim", 
    "curl", "wget",
    "zip", "unzip", "p7zip",
    "pciutils",

    # Apps:
    "firefox",
    "kitty",
    "yazi", 
    "feh", "flameshot", "dunst", "lxappearance",
    "flatpak", "fastfetch"
]

yay_packages = [
    # Tela de bloqueio:
    "betterlockscreen",

    # Fontes
    "ttf-meslo-nerd-font-powerlevel10k", "ttf-firacode-nerd", "noto-fonts-cjk",
    "noto-fonts-emoji"
]

system_packages_to_enable = [
    "sddm",
    "NetworkManager",
    "bluetooth",
    "ufw"
]

user_packages_to_enable = [
    "pipewire",
    "pipewire-pulse",
    "wireplumber"
]

stow_packages = [
    ("bspwm", ".config/bspwm"), 
    ("sxhkd", ".config/sxhkd"),
    ("picom", ".config/picom"), 
    ("polybar", ".config/polybar"), 
    ("rofi", ".config/rofi"),
    ("git", ".gitconfig"), 
    ("kitty", ".config/kitty"), 
    ("bash", ".bashrc", ".bash_profile"), 
    ("yazi", ".config/yazi")
]

packages_to_setup = [
    (
        "ufw", 
        "sudo ufw default deny incoming",
        "sudo ufw default allow outgoing",
        "sudo ufw --force enable"
    ),
    (
        "betterlockscreen", 
        "betterlockscreen -u dotfiles/wallpapers/Kobayashi.jpg"
    ),
    (
        "flatpak", 
        "sudo flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo"
    )
]