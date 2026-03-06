#!/bin/bash

playlist=(
	"https://www.youtube.com/watch?v=7t5LgFdV2q8"
	"https://www.youtube.com/watch?v=VFOg6mHtZcA"
	"https://www.youtube.com/watch?v=PdKj1065-P4"
)

URL=${playlist[$RANDOM % ${#playlist[@]}]}

(
	notify-send -i "audio-x-generic" "Receba" "$(yt-dlp --get-title "$URL")"
) &
mpv --no-video "$URL"
