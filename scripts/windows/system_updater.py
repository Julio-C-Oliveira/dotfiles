#!/usr/bin/env python3
"""
system_updater.py - Gerenciador e Notificador de Atualizações para Arch Linux
Integração com Rofi, Kitty, Pacman, Yay e Flatpak.
"""

import concurrent.futures
import html
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys


def escape_pango(text: str) -> str:
  return html.escape(text)


def check_pacman() -> list[str]:
  """Verifica atualizações nos repositórios oficiais via checkupdates."""
  if not shutil.which("checkupdates"):
    return []
  try:
    res = subprocess.run(
        ["checkupdates"],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
        timeout=30,
    )
    if res.returncode == 0:
      return [l.strip() for l in res.stdout.strip().splitlines() if l.strip()]
  except Exception:
    pass
  return []


def check_yay() -> list[str]:
  """Verifica atualizações no AUR via yay -Qua."""
  if not shutil.which("yay"):
    return []
  try:
    res = subprocess.run(
        ["yay", "-Qua"],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
        timeout=45,
    )
    if res.returncode == 0:
      return [l.strip() for l in res.stdout.strip().splitlines() if l.strip()]
  except Exception:
    pass
  return []


def check_flatpak() -> list[dict]:
  """Verifica atualizações do Flatpak via flatpak remote-ls --updates."""
  if not shutil.which("flatpak"):
    return []
  try:
    res = subprocess.run(
        [
            "flatpak",
            "remote-ls",
            "--updates",
            "--columns=name,version,application",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
        timeout=30,
    )
    if res.returncode == 0:
      lines = [l.strip() for l in res.stdout.strip().splitlines() if l.strip()]
      if lines and any(h in lines[0] for h in ["Nome", "Name", "ID"]):
        lines = lines[1:]

      results = []
      for line in lines:
        parts = [p.strip() for p in line.split("\t") if p.strip()]
        if not parts:
          continue
        name = parts[0]
        version = ""
        app_id = ""
        if len(parts) == 2:
          app_id = parts[1]
        elif len(parts) >= 3:
          version = parts[1]
          app_id = parts[2]
        results.append({"name": name, "version": version, "id": app_id})
      return results
  except Exception:
    pass
  return []


def format_pkg_line(raw_line: str) -> tuple[str, str, str]:
  """Formata linhas do tipo 'pacote versão_antiga -> versão_nova'."""
  match = re.match(r"^(\S+)\s+(\S+)\s+->\s+(\S+)$", raw_line)
  if match:
    pkg, old_ver, new_ver = match.groups()
    return pkg, old_ver, new_ver
  parts = raw_line.split()
  if parts:
    return parts[0], "", ""
  return raw_line, "", ""


def run_update_in_terminal(command: str, title: str) -> None:
  """Abre o Kitty executando a atualização de forma interativa."""
  kitty_bin = shutil.which("kitty") or "x-terminal-emulator"
  bash_script = f"""
echo -e "\\033[1;35m===================================================\\033[0m"
echo -e "\\033[1;35m   🔄 Atualização do Sistema: {title}\\033[0m"
echo -e "\\033[1;35m===================================================\\033[0m\\n"
echo -e "\\033[1;34m>> Executando: {command}\\033[0m\\n"

{command}
exit_code=$?

echo ""
if [ $exit_code -eq 0 ]; then
    echo -e "\\033[1;32m✔ Atualização concluída com sucesso!\\033[0m"
else
    echo -e "\\033[1;31m✖ Processo finalizado com erro (código: $exit_code).\\033[0m"
fi

echo ""
read -r -p "Pressione [Enter] para fechar..." _dummy
"""
  subprocess.Popen(
      [
          kitty_bin,
          "-o",
          "progress_bar=hidden",
          "-o",
          "window_title_template={title}",
          "-T",
          f"Atualização - {title}",
          "bash",
          "-c",
          bash_script,
      ]
  )


def notify_checking() -> None:
  if shutil.which("notify-send"):
    subprocess.run(
        [
            "notify-send",
            "-t",
            "1500",
            "-a",
            "Atualizações",
            "🔍 Verificando atualizações...",
            "Consultando Pacman, AUR e Flatpak...",
        ],
        check=False,
    )


def main():
  # Feedback imediato
  notify_checking()

  # Consulta concorrente para agilidade
  with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    fut_pacman = executor.submit(check_pacman)
    fut_yay = executor.submit(check_yay)
    fut_flatpak = executor.submit(check_flatpak)

    pacman_list = fut_pacman.result()
    yay_list = fut_yay.result()
    flatpak_list = fut_flatpak.result()

  total = len(pacman_list) + len(yay_list) + len(flatpak_list)

  menu_items = []
  actions = {}

  if total == 0:
    # Caso não haja nenhuma atualização pendente
    menu_items.append(
        "<b><span foreground='#50fa7b'>✨ Sistema 100% atualizado!</span></b>"
        "  <span foreground='#6272a4'>(Nenhuma atualização pendente)</span>"
    )
    actions[0] = None

    menu_items.append(
        "<b><span foreground='#bd93f9'>🔄 Sincronizar bases e verificar"
        " novamente</span></b>"
    )
    actions[1] = ("yay -Sy", "Sincronização de Bases")
  else:
    # 1. Opção global: Atualizar tudo
    all_cmds = []
    if pacman_list or yay_list:
      all_cmds.append("yay -Syu")
    if flatpak_list:
      all_cmds.append("flatpak update")
    full_cmd = " && ".join(all_cmds)

    summary_counts = []
    if pacman_list:
      summary_counts.append(f"{len(pacman_list)} Pacman")
    if yay_list:
      summary_counts.append(f"{len(yay_list)} AUR")
    if flatpak_list:
      summary_counts.append(f"{len(flatpak_list)} Flatpak")
    summary_str = ", ".join(summary_counts)

    idx = len(menu_items)
    menu_items.append(
        f"<b><span foreground='#50fa7b'>🚀 Atualizar Tudo</span></b>  <span"
        f" foreground='#bd93f9'>[{summary_str}]</span>"
    )
    actions[idx] = (full_cmd, "Tudo")

    # 2. Opções específicas por gerenciador
    if pacman_list:
      idx = len(menu_items)
      menu_items.append(
        f"<b><span foreground='#8be9fd'>📦 Atualizar Pacman</span></b>  <span"
        f" foreground='#f8f8f2'>({len(pacman_list)} pacotes oficiais)</span>"
      )
      actions[idx] = ("sudo pacman -Syu", "Pacman")

    if yay_list:
      idx = len(menu_items)
      menu_items.append(
        f"<b><span foreground='#ff79c6'>🔮 Atualizar AUR (Yay)</span></b>  <span"
        f" foreground='#f8f8f2'>({len(yay_list)} pacotes AUR)</span>"
      )
      actions[idx] = ("yay -Sua", "AUR (Yay)")

    if flatpak_list:
      idx = len(menu_items)
      menu_items.append(
        f"<b><span foreground='#f1fa8c'>📱 Atualizar Flatpak</span></b>  <span"
        f" foreground='#f8f8f2'>({len(flatpak_list)} aplicativos)</span>"
      )
      actions[idx] = ("flatpak update", "Flatpak")

    # 3. Lista detalhada de pacotes
    if pacman_list:
      menu_items.append(
          "<span foreground='#6272a4'>── Pacotes Oficiais (Pacman)"
          " ───────────────────────────────────</span>"
      )
      actions[len(menu_items) - 1] = None
      for raw in pacman_list:
        pkg, old_v, new_v = format_pkg_line(raw)
        idx = len(menu_items)
        if old_v and new_v:
          line = (
              f"  <span foreground='#8be9fd'>📦</span> <b><span"
              f" foreground='#f8f8f2'>{escape_pango(pkg)}</span></b> <span"
              f" foreground='#ff5555'>{escape_pango(old_v)}</span> <span"
              f" foreground='#50fa7b'>➜</span> <span"
              f" foreground='#50fa7b'>{escape_pango(new_v)}</span>"
          )
        else:
          line = (
              f"  <span foreground='#8be9fd'>📦</span> <b><span"
              f" foreground='#f8f8f2'>{escape_pango(raw)}</span></b>"
          )
        menu_items.append(line)
        actions[idx] = ("sudo pacman -Syu", "Pacman")

    if yay_list:
      menu_items.append(
          "<span foreground='#6272a4'>── Pacotes AUR (Yay)"
          " ──────────────────────────────────────────</span>"
      )
      actions[len(menu_items) - 1] = None
      for raw in yay_list:
        pkg, old_v, new_v = format_pkg_line(raw)
        idx = len(menu_items)
        if old_v and new_v:
          line = (
              f"  <span foreground='#ff79c6'>🔮</span> <b><span"
              f" foreground='#f8f8f2'>{escape_pango(pkg)}</span></b> <span"
              f" foreground='#ff5555'>{escape_pango(old_v)}</span> <span"
              f" foreground='#50fa7b'>➜</span> <span"
              f" foreground='#50fa7b'>{escape_pango(new_v)}</span>"
          )
        else:
          line = (
              f"  <span foreground='#ff79c6'>🔮</span> <b><span"
              f" foreground='#f8f8f2'>{escape_pango(raw)}</span></b>"
          )
        menu_items.append(line)
        actions[idx] = ("yay -Sua", "AUR (Yay)")

    if flatpak_list:
      menu_items.append(
          "<span foreground='#6272a4'>── Aplicativos Flatpak"
          " ──────────────────────────────────────</span>"
      )
      actions[len(menu_items) - 1] = None
      for item in flatpak_list:
        idx = len(menu_items)
        name = escape_pango(item['name'])
        app_id = escape_pango(item['id'])
        version = escape_pango(item['version'])
        ver_str = (
            f" <span foreground='#50fa7b'>[{version}]</span>" if version else ""
        )
        line = (
            f"  <span foreground='#f1fa8c'>📱</span> <b><span"
            f" foreground='#f8f8f2'>{name}</span></b>{ver_str} <span"
            f" foreground='#6272a4'>({app_id})</span>"
        )
        menu_items.append(line)
        actions[idx] = ("flatpak update", "Flatpak")

  menu_input = "\n".join(menu_items)

  rofi_cmd = [
      "rofi",
      "-dmenu",
      "-i",
      "-markup-rows",
      "-format",
      "i",
      "-p",
      f"🔄 Atualizações ({total})",
      "-theme-str",
      """
        window { 
            width: 70%; 
        }
        listview { 
            lines: 15; 
            columns: 1; 
            spacing: 3px;
        }
        element { 
            padding: 6px 12px; 
            border-radius: 4px;
        }
        entry { 
            placeholder: "Selecione uma atualização ou pressione Esc para sair..."; 
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
      cmd, title = action_info
      run_update_in_terminal(cmd, title)


if __name__ == "__main__":
  main()
