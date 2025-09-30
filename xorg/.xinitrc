#!bin/bash

# Variáveis de sessão XDG:
export XDG_SESSION_TYPE=x11
export XDG_CURRENT_DESKTOP=i3
export XDG_SESSION_DESKTOP=i3
export XDG_SESSION_CLASS=user
export XDG_RUNTIME_DIR=/run/user/$(id -u)

# Váriaveis gerais:
export EDITOR=nvim

# D-Bus:
if [ -z "$DBUS_SESSION_BUS_ADDRESS" ]; then
    eval "$(dbus-launch --sh-syntax --exit-with-session)"
fi

# Teclado:
setxkbmap -layout br -variant abnt2 -option lv3:ralt_switch

# Monitores:
xrandr --output DP2 --primary --auto --output VGA1 --auto --left-of DP2

# Papel de Parede:
feh --bg-fill ~/dotfiles/wallpapers/Kobayashi.jpg

# Path do usuário:
export PATH="$HOME/.local/bin:$PATH"

# Perfil de cores:
export GTK_THEME=Adwaita:dark
# export QT_QPA_PLATFORMTHEME=qt5ct

# Serviços

# Iniciando o i3-wn na home:
cd ~
exec i3
