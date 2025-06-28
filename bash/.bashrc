#
# ~/.bashrc
#

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

alias ls='ls --color=auto'
alias grep='grep --color=auto'
# PS1='[\u@\h \W]\$ '
PS1='\[\e[35m\]\u\e[36m\]@\h\[\e[0m\] \w \$ '
export PATH="$PATH:$HOME/.config/composer/vendor/bin"
