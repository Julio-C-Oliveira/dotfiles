#!/bin/bash

# O que eu preciso pro i3 rodar e logar fácil?
# [x] xorg -> servidor gráfico
# [x] sddm -> gerenciador de sessão

# O que eu tenho no meu i3?
# [x] Meslo LGM Nerd Font 12 -> a fonte que eu uso
# [x] Polybar -> launch.sh
# [x] xrandr -> Espelhamento de telas
# [x] feh -> carregar meu papel de parede
# [x] kitty -> o terminal que eu uso
# [x] rofi -> meu navegador de apps
# [x] betterlockscreen -> meu bloqueio de tela
# [x] flameshot -> meu print

# Qual deve ser a ordem?
# 0. yay -> repositório da comunidade do arch.
# 1. xorg -> sem ele não tem como usar os outros.
# 2. i3 -> é o gerenciador de janelas.
# 3. Meslo LGM Nerd Font 12 -> precisa só do i3.
# 4. feh -> só precisa do i3.
# 5. betterlockscreen -> só precisa do i3.
# 6. flasmeshot -> só precisa do i3.
# 7. polybar -> só precisa do i3.
# 8. rofi -> só precisa do i3.
# 9. kitty -> só precisa do i3 e da fonte.
# 10. yazi -> navegador básico de arquivos.
# 11. vim -> editor básico de textos.
# 12. xrandr -> opcional.
# 13. sddm -> gerenciador de login, precisa do xorg e do i3.
# 14. stow -> gerenciador de links simbolicos.
# 15. flathub -> flatpacks. 



# O Script inicia aqui:

# Controla alguns pontos do script:
# -e -> para o script se algum comando falhar.
# -u -> se alguma variavel não estiver definida gera erro.
# -o pipefail -> se algum comando em um pipeline gerar erro, retorna erro.
set -euo pipefail


# Atualizar o sistema:
# - noconfirm, responde sim para as perguntas padrão que ocorrem durante a instalação.
sudo pacman -Syu --noconfirm


# Instalando o yay:
# É um repositório extra, feito pela comunidade do arch.
# - git, é um gerenciador de versionamento de código.
# - base-devel, é um pacote com várias ferramentas necessárias, para compilar programas.
# - needed, caso já esteja instalado, não reinstala.
# - s, instala as dependências necessárias.
# - i, instala o pacote, depois de compilar.
sudo pacman -S --needed --noconfirm git base-devel

if ! command -v yay &>/dev/null; then
    sudo rm -rf /tmp/yay
    git clone https://aur.archlinux.org/yay.git /tmp/yay
    cd /tmp/yay
    makepkg -si --noconfirm
    cd -
fi


# Instalando os pacotes necessários:
# - xorg-server, é o motor gráfico do sistema.
# - xorg-xrandr, serve pra gerenciar os monitores.
# - xf86-input-libinput, driver de teclado e mouse pro xorg.
# - i3-wm, é um tilling window manager, responsável por gerar e controlar as janelas.
# - feh, é um visualizador de imagens.
# - betterlockscreen, bloqueia a tela.
# - flameshot, é um app de print.
# - polybar, substitui o i3bar, acho mais bonito.
# - rofi, substitui o dmenu, acho mais bonito.
# - kitty, é um emulador de terminal, que consegue exibir imagens.
# - yazi, é um navegador de arquivos.
# - vim, é um editor de texto.
# - stow, é um gerenciador de dotfiles, via links simbolicos.
# - flatpak, é um sistema de empacotamento e distribuição de aplicativos.
# - curl, serve pra baixar e enviar arquivos pelo terminal.
# - sddm, é um gerenciador de login em ambiente gráfico.
sudo pacman -S --needed --noconfirm \
	xorg-server \
	xorg-xrandr \
	xf86-input-libinput \
	i3-wm \
	feh \
	flameshot \
	polybar \
	rofi \
	kitty \
	yazi \
	stow \
	flatpak \
	curl \
	sddm \
	qt5-graphicaleffects \
	qt5-quickcontrols2 \
	qt5-svg \
	ufw \
	gcc \
	make \
	ripgrep \
	fd \
	unzip \
	neovim \
	github-cli

yay -S --needed --noconfirm betterlockscreen


# Removendo os arquivos de configuração já existentes, que serão substituidos pelos meus:
# - rf, serve pra remover recursivamente, de modo forçado.
# - d e o f, servem para verificar se o diretório ou o arquivo existem.
[ -d ~/.config/i3 ] && rm -rf ~/.config/i3
[ -d ~/.config/polybar ] && rm -rf ~/.config/polybar
[ -d ~/.config/rofi ] && rm -rf ~/.config/rofi
[ -d ~/.config/kitty ] && rm -rf ~/.config/kitty
[ -f ~/.bashrc ] && rm -f ~/.bashrc
[ -f ~/.gitconfig] && rm -f ~/.gitconfig


# Baixando fontes e papéis de parede:
# - mkdir -p, cria a pasta, se ela não existir.
# Tenho que alterar a localização dos wallpapers no i3 também.
yay -S --needed --noconfirm ttf-meslo-nerd-font-powerlevel10k

mkdir -p wallpapers
bash gdrive_download.sh 1nlJ2Ch7wICBj6d4b8HM8dhSqga703mQ6 wallpapers/Kobayashi.jpg
bash gdrive_download.sh 1mJ6XrV1nBeRmHKTcsDIN1KJ1Hycfd9iW wallpapers/Rukia.jpg


# Criando os links simbolicos para os dotfiles:
mkdir -p ~/.config 
stow bash git
stow i3 polybar rofi kitty yazi


# Configurando o sddm:
sudo systemctl enable sddm.service

mkdir -p themes
bash gdrive_download.sh 17MaLG6VJw1z4ONtGYfPjVORI18eK_8ma themes/sugar-candy.tar.gz

sudo mkdir -p /usr/share/sddm/themes
sudo tar -xzvf themes/sugar-candy.tar.gz -C /usr/share/sddm/themes
sudo mkdir -p /etc/sddm.conf.d
sudo stow -t / sddm

sudo cp wallpapers/Rukia.jpg /usr/share/sddm/themes/sugar-candy/Backgrounds/Mountain.jpg


# Configurando o Betterlockscreen:
betterlockscreen -u wallpapers/Kobayashi.jpg


# Configurando o ufw:
sudo systemctl enable ufw


# Configurando o nvim:
git clone https://github.com/nvim-lua/kickstart.nvim.git "${XDG_CONFIG_HOME:-$HOME/.config}"/nvim


# Adicionando o flathub:
sudo flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo


# Avisando o user de que a instalação foi finalizada:
echo "Instalação concluída com sucesso. O dispositivo será reiniciado em 5 segundos."
sleep 5
reboot
