#!/bin/bash

pkill -f -v $$ change_wallpaper.sh

folder_path="${1:-${HOME}/dotfiles/wallpapers}"
sleep_time="${2:-25}"

wallpapers_path=("$folder_path"/*)

while true; do
	selected_wallpaper="${wallpapers_path[RANDOM % ${#wallpapers_path[@]}]}"

	feh --bg-fill $selected_wallpaper
	sleep $sleep_time
done
