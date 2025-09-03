#!/bin/bash

set -euo pipefail # Parar o script em caso de erro.

# 1. Atualizar o sistema:
sudo pacman -Syu --noconfirm

# 2. Instalando os pacotes necessários:
# - Xorg, é o motor gráfico do sistema.
# - i3, é um tilling window manager, responsável por controlar as janelas.
# - stow, é um gerenciador de dotfiles, via links simbolicos.
sudo pacman -S --noconfirm \
	xorg \
	i3 \
	stow

# 3. Removendo os arquivos de configuração já existentes:
# -rf, serve pra remover recursivamente, de modo forçado.
# -f, remover de modo forçado.
rm -rf ~/.config/i3
rm -f ~/.bashrc

# 4. Avisando o user de que a instalação foi finalizada:
echo "Instalação concluída com sucessso."
