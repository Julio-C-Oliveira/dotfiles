#!/bin/sh

# =============================================================================
# bspwm_monitor_setup.sh
#
# Detecta monitores conectados via xrandr, os posiciona automaticamente
# em sequência (right-of) e atribui os desktops 1–10 a cada um no bspwm.
#
# Uso: chamado pelo bspwmrc na inicialização.
# Também pode ser chamado manualmente ao conectar/desconectar um monitor.
# =============================================================================

# Obtém os nomes dos monitores conectados, na ordem que o xrandr os lista
connected=$(xrandr | awk '/ connected/{print $1}')

if [ -z "$connected" ]; then
    echo "bspwm_monitor_setup: nenhum monitor conectado detectado." >&2
    exit 1
fi

# Posiciona os monitores: o primeiro é o primário, os demais ficam à direita
prev=""
for mon in $connected; do
    if [ -z "$prev" ]; then
        xrandr --output "$mon" --primary --auto
    else
        xrandr --output "$mon" --auto --right-of "$prev"
    fi
    prev="$mon"
done

# Desativa monitores que estavam conectados mas não estão mais
xrandr | awk '/ disconnected/{print $1}' | while read -r mon; do
    xrandr --output "$mon" --off
done

# Aguarda o bspwm reconhecer os monitores após o xrandr
sleep 0.5

# Atribui os desktops 1–10 a cada monitor registrado no bspwm
for mon in $(bspc query -M --names); do
    bspc monitor "$mon" -d 1 2 3 4 5 6 7 8 9 10
done
