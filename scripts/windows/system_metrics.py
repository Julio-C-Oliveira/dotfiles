#!/usr/bin/env python3
"""
system_metrics.py - Painel Rofi de Métricas do Sistema
Exibe uso de disco detalhado, layout do teclado e métricas separadas de Wi-Fi e Ethernet.
"""

import html
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys


def escape_pango(text: str) -> str:
  return html.escape(str(text))


def format_bytes(bytes_val: int) -> str:
  for unit in ["B", "KB", "MB", "GB", "TB"]:
    if bytes_val < 1024 or unit == "TB":
      return f"{bytes_val:.1f} {unit}" if unit in ["GB", "TB"] else f"{bytes_val:.0f} {unit}"
    bytes_val /= 1024
  return f"{bytes_val:.1f} GB"


def get_disk_info() -> list[dict]:
  disks = []
  partitions = ["/", "/home", "/boot"]
  for path in partitions:
    if os.path.exists(path):
      try:
        du = shutil.disk_usage(path)
        pct = (du.used / du.total) * 100
        disks.append({
            "path": path,
            "total": format_bytes(du.total),
            "used": format_bytes(du.used),
            "free": format_bytes(du.free),
            "pct": pct,
        })
      except Exception:
        pass
  return disks


def get_keyboard_layout() -> dict:
  layout = "desconhecido"
  model = ""
  try:
    res = subprocess.run(
        ["setxkbmap", "-query"], capture_output=True, text=True, timeout=1
    )
    for line in res.stdout.splitlines():
      if "layout:" in line:
        layout = line.split(":", 1)[1].strip()
      elif "model:" in line:
        model = line.split(":", 1)[1].strip()
  except Exception:
    pass
  return {"layout": layout, "model": model}


def get_ip_address(iface: str) -> str:
  try:
    res = subprocess.run(
        ["ip", "-br", "addr", "show", iface],
        capture_output=True,
        text=True,
        timeout=1,
    )
    parts = res.stdout.split()
    if len(parts) >= 3:
      return parts[2].split("/")[0]
  except Exception:
    pass
  return ""


def get_wifi_details() -> dict:
  ssid = ""
  signal = ""
  iface = "wlp0s20f3"

  # Tenta localizar interface wireless
  for p in Path("/sys/class/net").glob("wl*"):
    iface = p.name
    break

  try:
    res = subprocess.run(
        ["nmcli", "-t", "-f", "ACTIVE,SSID,SIGNAL", "dev", "wifi"],
        capture_output=True,
        text=True,
        env={**os.environ, "LC_ALL": "C"},
        timeout=2,
    )
    for line in res.stdout.splitlines():
      if line.startswith("yes:"):
        parts = line.split(":")
        if len(parts) >= 3:
          ssid = parts[1]
          signal = parts[2]
        break
  except Exception:
    pass

  ip_addr = get_ip_address(iface)
  connected = bool(ssid)

  return {
      "iface": iface,
      "connected": connected,
      "ssid": ssid,
      "signal": signal,
      "ip": ip_addr,
  }


def get_ethernet_details() -> dict:
  iface = "eth0"
  for p in Path("/sys/class/net").glob("e*"):
    if p.name != "lo":
      iface = p.name
      break

  operstate_file = Path(f"/sys/class/net/{iface}/operstate")
  is_up = False
  if operstate_file.exists():
    try:
      is_up = operstate_file.read_text().strip().lower() == "up"
    except Exception:
      pass

  speed_str = ""
  speed_file = Path(f"/sys/class/net/{iface}/speed")
  if is_up and speed_file.exists():
    try:
      speed_val = speed_file.read_text().strip()
      if speed_val.isdigit():
        speed_str = f"{speed_val} Mb/s"
    except Exception:
      pass

  ip_addr = get_ip_address(iface)

  return {
      "iface": iface,
      "connected": is_up,
      "speed": speed_str,
      "ip": ip_addr,
  }


def get_total_network_traffic() -> dict:
  rx_total = 0
  tx_total = 0
  try:
    with open("/proc/net/dev", "r") as f:
      for line in f.readlines()[2:]:
        parts = line.split(":")
        if len(parts) == 2:
          dev = parts[0].strip()
          if dev == "lo" or dev.startswith(("docker", "br-", "veth")):
            continue
          vals = parts[1].split()
          rx_total += int(vals[0])
          tx_total += int(vals[8])
  except Exception:
    pass
  return {"rx": format_bytes(rx_total), "tx": format_bytes(tx_total)}


def toggle_keyboard_layout(current_layout: str) -> None:
  new_layout = "us" if current_layout == "br" else "br"
  try:
    subprocess.run(["setxkbmap", new_layout], check=True)
    subprocess.run(
        [
            "notify-send",
            "-a",
            "Teclado",
            "Layout Alterado",
            f"Layout alterado para: {new_layout.upper()}",
        ],
        check=False,
    )
  except Exception as e:
    subprocess.run(
        [
            "notify-send",
            "-a",
            "Teclado",
            "Erro ao alternar layout",
            str(e),
        ],
        check=False,
    )


def open_nmtui() -> None:
  kitty_bin = shutil.which("kitty") or "x-terminal-emulator"
  subprocess.Popen(
      [kitty_bin, "-T", "Gerenciador de Redes (nmtui)", "nmtui"]
  )


def open_file_manager(target_path: str = "/") -> None:
  kitty_bin = shutil.which("kitty") or "x-terminal-emulator"
  if shutil.which("yazi"):
    subprocess.Popen([kitty_bin, "-T", f"Yazi - {target_path}", "yazi", target_path])
  else:
    subprocess.Popen([kitty_bin, "-T", f"Disco - {target_path}", "bash", "-c", f"df -h {target_path}; echo; read -p 'Pressione Enter para fechar...'"])


def main():
  disks = get_disk_info()
  kb = get_keyboard_layout()
  wifi = get_wifi_details()
  eth = get_ethernet_details()
  traffic = get_total_network_traffic()

  menu_items = []
  actions = {}

  # 1. Seção de Disco
  menu_items.append(
      "<b><span foreground='#bd93f9'>💾 ARMAZENAMENTO (DISCO)</span></b>"
  )
  actions[len(menu_items) - 1] = None

  for d in disks:
    pct = d["pct"]
    color = "#50fa7b" if pct < 70 else ("#f1fa8c" if pct < 85 else "#ff5555")
    name = "/" if d["path"] == "/" else d["path"]
    line = (
        f"  <span foreground='#8be9fd'>📁</span> <b><span"
        f" foreground='#f8f8f2'>{name:<8}</span></b>"
        f" <span foreground='{color}'>{d['used']:>8} / {d['total']:<8}"
        f" ({pct:.0f}%)</span>  <span foreground='#6272a4'>[Livre:"
        f" {d['free']}]</span>"
    )
    idx = len(menu_items)
    menu_items.append(line)
    actions[idx] = ("open_disk", d["path"])

  # 2. Seção de Teclado
  menu_items.append("")
  actions[len(menu_items) - 1] = None

  menu_items.append(
      "<b><span foreground='#bd93f9'>⌨️ TECLADO</span></b>"
  )
  actions[len(menu_items) - 1] = None

  current_kb = kb["layout"].upper()
  model_info = f" ({kb['model']})" if kb['model'] else ""
  kb_line = (
      f"  <span foreground='#50fa7b'>󰌌</span> <b><span"
      f" foreground='#f8f8f2'>Layout Atual: {current_kb}</span></b><span"
      f" foreground='#6272a4'>{model_info}</span>  <span"
      f" foreground='#ff79c6'>[Clique para alternar br/us]</span>"
  )
  idx = len(menu_items)
  menu_items.append(kb_line)
  actions[idx] = ("toggle_kb", kb["layout"])

  # 3. Seção de Rede Wi-Fi
  menu_items.append("")
  actions[len(menu_items) - 1] = None

  menu_items.append(
      "<b><span foreground='#bd93f9'>📡 WI-FI</span></b>"
  )
  actions[len(menu_items) - 1] = None

  if wifi["connected"]:
    sig_str = f"Sinal: {wifi['signal']}%" if wifi['signal'] else "Conectado"
    ip_str = f"IP: {wifi['ip']}" if wifi['ip'] else ""
    wifi_line = (
        f"  <span foreground='#50fa7b'>󰤨</span> <b><span"
        f" foreground='#f8f8f2'>{escape_pango(wifi['ssid'])}</span></b> "
        f" <span foreground='#8be9fd'>[{sig_str}]</span>  <span"
        f" foreground='#f1fa8c'>{ip_str}</span>"
    )
  else:
    wifi_line = (
        f"  <span foreground='#6272a4'>󰤮</span> <span"
        f" foreground='#6272a4'>Wi-Fi Desconectado ({wifi['iface']})</span>"
    )
  idx = len(menu_items)
  menu_items.append(wifi_line)
  actions[idx] = ("open_net", None)

  # 4. Seção de Rede Cabeada
  menu_items.append("")
  actions[len(menu_items) - 1] = None

  menu_items.append(
      "<b><span foreground='#bd93f9'>🔌 REDE CABEADA (ETHERNET)</span></b>"
  )
  actions[len(menu_items) - 1] = None

  if eth["connected"]:
    spd_str = f"[{eth['speed']}]" if eth['speed'] else "[Conectado]"
    ip_str = f"IP: {eth['ip']}" if eth['ip'] else ""
    eth_line = (
        f"  <span foreground='#50fa7b'>󰛳</span> <b><span"
        f" foreground='#f8f8f2'>{eth['iface']}</span></b>  <span"
        f" foreground='#8be9fd'>{spd_str}</span>  <span"
        f" foreground='#f1fa8c'>{ip_str}</span>"
    )
  else:
    eth_line = (
        f"  <span foreground='#6272a4'>󰲛</span> <span"
        f" foreground='#6272a4'>Ethernet Desconectada ({eth['iface']})</span>"
    )
  idx = len(menu_items)
  menu_items.append(eth_line)
  actions[idx] = ("open_net", None)

  # 5. Seção de Tráfego Geral Acumulado
  menu_items.append("")
  actions[len(menu_items) - 1] = None

  menu_items.append(
      "<b><span foreground='#bd93f9'>🌐 TRÁFEGO TOTAL DA SESSÃO</span></b>"
  )
  actions[len(menu_items) - 1] = None

  traffic_line = (
      f"  <span foreground='#8be9fd'>󰒢</span>  Download (RX): <span"
      f" foreground='#50fa7b'><b>{traffic['rx']}</b></span>  |  Upload (TX):"
      f" <span foreground='#ff79c6'><b>{traffic['tx']}</b></span>"
  )
  idx = len(menu_items)
  menu_items.append(traffic_line)
  actions[idx] = ("open_net", None)

  menu_input = "\n".join(menu_items)

  rofi_cmd = [
      "rofi",
      "-dmenu",
      "-i",
      "-markup-rows",
      "-format",
      "i",
      "-p",
      "📊 Métricas do Sistema",
      "-theme-str",
      """
        window { 
            width: 70%; 
        }
        listview { 
            lines: 16; 
            columns: 1; 
            spacing: 2px;
        }
        element { 
            padding: 5px 12px; 
            border-radius: 4px;
        }
        entry { 
            placeholder: "Visualizar métricas ou selecionar para abrir gerenciador..."; 
        }
      """,
  ]

  res = subprocess.run(
      rofi_cmd, input=menu_input, text=True, capture_output=True
  )

  if res.returncode == 0 and res.stdout.strip().isdigit():
    idx = int(res.stdout.strip())
    action_info = actions.get(idx)
    if action_info:
      action_type, action_val = action_info
      if action_type == "toggle_kb":
        toggle_keyboard_layout(action_val)
      elif action_type == "open_disk":
        open_file_manager(action_val)
      elif action_type == "open_net":
        open_nmtui()


if __name__ == "__main__":
  main()
