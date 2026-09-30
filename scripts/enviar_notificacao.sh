#!/bin/bash

# ==============================================================================
# Script para enviar notificação de trabalho (GUI) para outro usuário logado
# Uso: ./enviar_notificacao.sh <usuario_destino> <remetente> <mensagem>
# Exemplo: ./enviar_notificacao.sh luiz "Julio" "Banda Desejo de Menina. Gaga >> Luiz."
# ==============================================================================

TARGET_USER="$1"
SENDER_NAME="$2"
MESSAGE="$3"

# Validação dos parâmetros
if [ -z "$TARGET_USER" ] || [ -z "$SENDER_NAME" ] || [ -z "$MESSAGE" ]; then
    echo "Uso: $0 <usuario_destino> <remetente> <mensagem>"
    echo "Exemplo: $0 luiz \"Julio\" \"Banda Desejo de Menina. Gaga >> Luiz.\""
    exit 1
fi

# Verifica se o usuário existe no sistema
if ! id "$TARGET_USER" >/dev/null 2>&1; then
    echo "Erro: O usuário '$TARGET_USER' não existe neste sistema." >&2
    exit 1
fi

TARGET_UID=$(id -u "$TARGET_USER")

# Tenta identificar o DISPLAY ativo do usuário destino automaticamente
TARGET_PID=$(pgrep -u "$TARGET_USER" | head -n1)
if [ -n "$TARGET_PID" ] && [ -r "/proc/$TARGET_PID/environ" ]; then
    TARGET_DISP=$(grep -z "^DISPLAY=" "/proc/$TARGET_PID/environ" 2>/dev/null | cut -d= -f2)
fi

# Fallback para :0 caso não encontre o DISPLAY
[ -z "$TARGET_DISP" ] && TARGET_DISP=":0"

# Executa o notify-send na sessão visual do usuário destino
sudo -u "$TARGET_USER" \
    DISPLAY="$TARGET_DISP" \
    DBUS_SESSION_BUS_ADDRESS="unix:path=/run/user/$TARGET_UID/bus" \
    notify-send "Mensagem de $SENDER_NAME" "$MESSAGE"
