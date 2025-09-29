#!/bin/bash

# Uso: disk-usage.sh <state> <percentual_alerta> "<icone_normal> <icone_alerta>" "<cor_normal> <cor_alerta>" "<part1> <part2> ..."


# Parâmetros:
# state: 0 é o simplificado e 1 é o detalhado.
# warn: quando deve ocorrer a mudaça pra alerta.
# icons: o primeiro é o normal e o segundo o de alerta.
# partitions: são as partições
state="${1:-0}"
warn="${2:-75}"
icons=($3)
normal_icon="${icons[0]:-󰗮}"
alert_icon="${icons[1]:-󰇑}"
colors=($4)
normal_color="${colors[0]:-#9BBF65}"
alert_color="${colors[1]:-#F28963}"
partitions=($5)

icon=$normal_icon
icon_color=$normal_color
max_disk_use=0

for partition in "${partitions[@]}"; do
	disk_use=$(df "$partition" --output=pcent | tail -1 | tr -dc '0-9')
	if [ "$disk_use" -gt "$max_disk_use" ]; then
		max_disk_use=$disk_use
	fi
done

if [ "$max_disk_use" -ge "$warn" ]; then
	icon=$alert_icon
	icon_color=$alert_color
else
	icon=$normal_icon
	icon_color=$normal_color
fi

total_disk_usage=$(df --total --output=used | tail -1)
total_free_disk=$(df --total --output=avail | tail -1)
percentage=$(( total_disk_usage * 100 / (total_disk_usage + total_free_disk) ))

if [ "$state" == "0" ]; then
	echo "%{F$icon_color}$icon%{F-} $percentage%"
elif [ "$state" == "1" ]; then
	echo "Executando clique" > ~/teste.txt
	click_command="'df -h / /home | awk 'NR>1 {print $6 ": " $5}' | paste -sd ' ''"
	echo "$click_command"
else
	echo "%{F$icon_color}$icon%{F-} $percentage%"
fi
