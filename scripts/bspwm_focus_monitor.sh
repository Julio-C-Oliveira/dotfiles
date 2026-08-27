#!/bin/sh

# =============================================================================
# bspwm_focus_monitor.sh
#
# Foca o próximo ou anterior monitor no bspwm E move o cursor do mouse
# para o centro dele, evitando que o foco reverta pela posição do mouse.
#
# Uso: bspwm_focus_monitor.sh [next|prev]
# Depende de: bspc, xrandr, python3 (ou xdotool como alternativa)
# =============================================================================

direction="${1:-next}"

# Foca o monitor no bspwm
bspc monitor -f "$direction"

# Obtém o nome do monitor agora focado
mon=$(bspc query -M -m focused --names)

# Extrai a geometria do monitor via xrandr e calcula o centro
geom=$(xrandr | awk -v target="$mon" '
    $1 == target && / connected / {
        match($0, /([0-9]+)x([0-9]+)\+([0-9]+)\+([0-9]+)/, a)
        print a[3] + int(a[1]/2), a[4] + int(a[2]/2)
        exit
    }
')

x=$(echo "$geom" | cut -d' ' -f1)
y=$(echo "$geom" | cut -d' ' -f2)

if [ -z "$x" ] || [ -z "$y" ]; then
    exit 0
fi

# Move o cursor para o centro do monitor
# Tenta xdotool primeiro; cai para python3+libX11 se não estiver disponível
if command -v xdotool > /dev/null 2>&1; then
    xdotool mousemove "$x" "$y"
else
    python3 - "$x" "$y" << 'EOF'
import ctypes, ctypes.util, sys
x, y = int(sys.argv[1]), int(sys.argv[2])
lib = ctypes.cdll.LoadLibrary(ctypes.util.find_library('X11'))
# Declarar tipos corretos para evitar truncamento de ponteiro em 64-bit
lib.XOpenDisplay.restype = ctypes.c_void_p
lib.XOpenDisplay.argtypes = [ctypes.c_char_p]
lib.XDefaultRootWindow.restype = ctypes.c_ulong
lib.XDefaultRootWindow.argtypes = [ctypes.c_void_p]
lib.XWarpPointer.argtypes = [ctypes.c_void_p, ctypes.c_ulong, ctypes.c_ulong,
                              ctypes.c_int, ctypes.c_int, ctypes.c_uint, ctypes.c_uint,
                              ctypes.c_int, ctypes.c_int]
lib.XFlush.argtypes = [ctypes.c_void_p]
lib.XCloseDisplay.argtypes = [ctypes.c_void_p]
d = lib.XOpenDisplay(None)
root = lib.XDefaultRootWindow(d)
lib.XWarpPointer(d, 0, root, 0, 0, 0, 0, x, y)
lib.XFlush(d)
lib.XCloseDisplay(d)
EOF
fi
