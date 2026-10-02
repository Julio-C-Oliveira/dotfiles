#!/usr/bin/env bash

# Configuração de áudio
if [ "$1" = "audio" ]; then
    export AUDIO_OPTS="--volume=40"
else
    export AUDIO_OPTS="--mute=yes"
fi

# Define o script do Bad Apple como protetor
export XSECURELOCK_SAVER="$HOME/.local/bin/bad_apple_saver"

# 1. Encerra o Picom para evitar buffer leaks e flashes no X11
killall picom 2>/dev/null

# 2. Executa o xsecurelock em foreground (o script pausa aqui até o desbloqueio)
xsecurelock 2>/dev/null

# 3. Assim que a tela é desbloqueada com sucesso, religa o compositor
picom -b &
