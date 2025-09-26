#
# ~/.bashrc
#

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

alias ls='ls --color=auto'
alias grep='grep --color=auto'

PS1='\[\e[35m\]\u\[\e[36m\]@\h\[\e[0m\] \W \$ '

export PATH="$HOME/.local/bin:$PATH"

# Funções extras:
clearscreenandscrollback() {
  clear
  printf '\033[3J' # Comando que limpa os comandos da tela e o scrollback. Simula o comportamento do gnome-terminal.
}
