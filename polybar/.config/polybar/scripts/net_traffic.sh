#!/usr/bin/env bash
# ==============================================================================
# net_traffic.sh - Monitor de tráfego geral de rede (combinado) para Polybar
# ==============================================================================

human_speed() {
    local bytes=$1
    if (( bytes < 1024 )); then
        echo "${bytes} B/s"
    elif (( bytes < 1048576 )); then
        echo "$(( (bytes + 512) / 1024 )) KB/s"
    else
        local mb=$(( bytes * 10 / 1048576 ))
        echo "$(( mb / 10 )).$(( mb % 10 )) MB/s"
    fi
}

get_bytes() {
    awk '
    NR > 2 {
        iface = $1
        sub(/:/, "", iface)
        if (iface !~ /^(lo|docker|br-|veth)/) {
            rx += $2
            tx += $10
        }
    }
    END { print rx + tx }
    ' /proc/net/dev
}

prev_bytes=$(get_bytes)

while true; do
    sleep 1
    curr_bytes=$(get_bytes)
    diff=$(( curr_bytes - prev_bytes ))
    if (( diff < 0 )); then diff=0; fi
    prev_bytes=$curr_bytes

    human_speed "$diff"
done
