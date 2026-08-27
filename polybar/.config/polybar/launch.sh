#!/bin/bash

# Mata as instâncias antigas da polybar
pkill -u "$USER" -x polybar

# Espera até elas serem fechadas
while pgrep -u "$USER" -x polybar >/dev/null; do sleep 1; done

# Inicia uma instância da polybar para cada monitor detectado
for mon in $(bspc query -M --names); do
    MONITOR=$mon polybar top_primary &
done
