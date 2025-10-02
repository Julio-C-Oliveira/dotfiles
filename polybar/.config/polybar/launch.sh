#!/bin/bash

# Mata as instâncias antigas da polybar
pkill -u "$USER" -x polybar

# Espera até elas serem fechadas
while pgrep -u "$USER" -x polybar >/dev/null; do sleep 1; done

# Inicia a polybar
polybar top_primary &
