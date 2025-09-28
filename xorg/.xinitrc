#!bin/bash

# Variáveis de sessão XDG:
export XDG_SESSION_TYPE=x11
export XDG_CURRENT_DESKTOP=
export XDG_SESSION_DESKTOP=
export XDG_SESSION_CLASS=
export XDG_RUNTIME_DIR=/run/user/$(id -u)

# D-Bus:
if [ -z "$DBUS_SESSION_BUS_ADDRESS" ]; then
    eval "$(dbus-launch --sh-syntax --exit-with-session)"
fi

# Teclado:
setxkbmap -layout br -variant abnt2 -option lv3:ralt_switch

# Monitores:
xrandr --output eDP-1 --primary --auto --output HDMI-2 --auto --left-of eDP-1

# Papel de Parede:
feh --bg-fill ~/dotfiles/wallpapers/Kobayashi.jpg

# Path do usuário
export PATH=$HOME/.local/bin:/usr/local/bin:/usr/bin:/usr/local/sbin:$PATH

# Serviços

# i3-wn
exec i3
