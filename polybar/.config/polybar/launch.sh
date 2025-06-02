#!/bin/bash

# Mata as instâncias antigas da polybar
killall -q polybar

# Espera até elas serem fechadas
while pgrep -x polybar >/dev/null; do sleep 1; done

# Inicia a polybar
polybar example &
