#!/bin/bash

if [ $# -ne 2 ]; then
    echo "Uso: $0 <FILE_ID> <NOME_DO_ARQUIVO>"
    exit 1
fi

FILE_ID="$1"
FILENAME="$2"

# URL inicial
URL="https://drive.google.com/uc?export=download&id=${FILE_ID}"

# Primeiro passo: pega token de confirmação, se houver
CONFIRM=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate \
    "$URL" -O- \
    | grep -Po '(?<=confirm=)[0-9A-Za-z_]+' | head -n1)

# Segundo passo: baixa o arquivo com token (se houver)
if [ -n "$CONFIRM" ]; then
    wget --load-cookies /tmp/cookies.txt "https://drive.google.com/uc?export=download&confirm=${CONFIRM}&id=${FILE_ID}" -O "${FILENAME}"
else
    wget "$URL" -O "${FILENAME}"
fi

# Verificação rápida
if file "${FILENAME}" | grep -q "HTML"; then
    echo "❌ Erro: baixou HTML em vez do arquivo real."
    exit 1
fi

echo "✅ Download concluído: ${FILENAME}"

