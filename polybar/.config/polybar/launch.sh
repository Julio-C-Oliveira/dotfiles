#!/bin/bash

# Mata as instâncias antigas da polybar
pkill -u "$USER" -x polybar

# Espera até elas serem fechadas
while pgrep -u "$USER" -x polybar >/dev/null; do sleep 1; done

# Detecta o monitor primário (ou o primeiro da lista como fallback)
primary_mon=$(bspc query -M -m primary --names 2>/dev/null || bspc query -M --names | head -n 1)

# Inicia top_primary na tela principal e top_secondary nas telas secundárias
for mon in $(bspc query -M --names); do
    if [ "$mon" = "$primary_mon" ]; then
        MONITOR=$mon polybar top_primary &
    else
        MONITOR=$mon polybar top_secondary &
    fi
done

disown -a
