#!/bin/bash

# Mata as instâncias antigas da polybar
pkill -u "$USER" -x polybar

# Espera até elas serem fechadas
while pgrep -u "$USER" -x polybar >/dev/null; do sleep 1; done

# Detecta o monitor primário (ou o primeiro da lista como fallback)
primary_mon=$(bspc query -M -m primary --names 2>/dev/null || bspc query -M --names | head -n 1)

# Inicia a polybar atribuindo o tray apenas para o monitor principal
for mon in $(bspc query -M --names); do
    if [ "$mon" = "$primary_mon" ]; then
        TRAY="tray"
    else
        TRAY=""
    fi
    MONITOR=$mon TRAY_MODULE=$TRAY polybar top_primary &
done
