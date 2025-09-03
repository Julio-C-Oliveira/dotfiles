#!/bin/bash

# Verifica se recebeu os dois argumentos
if [ $# -ne 2 ]; then
    echo "Uso: $0 <FILE_ID> <NOME_DO_ARQUIVO>"
    exit 1
fi

FILE_ID="$1"
FILENAME="$2"

# URL do Google Drive
CONFIRM=$(curl -sc /tmp/gcookie "https://drive.google.com/uc?export=download&id=${FILE_ID}" | \
          grep -o 'confirm=[^&]*' | head -n 1)

curl -Lb /tmp/gcookie "https://drive.google.com/uc?export=download&${CONFIRM}&id=${FILE_ID}" -o "${FILENAME}"

echo "Download concluído: ${FILENAME}"

