#!/usr/bin/env python3
"""
pomodoro_menu.py - Menu Rofi para Controle do Pomodoro
"""

import json
from pathlib import Path
import subprocess
import sys

POMODORO_SCRIPT = Path.home() / "dotfiles" / "scripts" / "pomodoro.py"
STATE_FILE = Path("/tmp/pomodoro_state.json")


def load_state() -> dict:
  if STATE_FILE.exists():
    try:
      with open(STATE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)
    except Exception:
      pass
  return {"state": "stopped", "mode": "work", "cycle_count": 0}


def run_pomodoro(args: list[str]):
  subprocess.run([str(POMODORO_SCRIPT)] + args)


def ask_custom_time() -> float | None:
  rofi_cmd = [
      "rofi",
      "-dmenu",
      "-p",
      "⏱️ Minutos",
      "-theme-str",
      """
        window { width: 30%; }
        listview { lines: 0; }
        entry { placeholder: "Digite a duração em minutos (ex: 30, 45, 10)..."; }
      """,
  ]
  res = subprocess.run(rofi_cmd, capture_output=True, text=True)
  if res.returncode == 0:
    val = res.stdout.strip()
    try:
      mins = float(val)
      if mins > 0:
        return mins
    except ValueError:
      pass
  return None


def main():
  state = load_state()
  st = state.get("state", "stopped")
  mode = state.get("mode", "work")
  cycles = state.get("cycle_count", 0)

  menu_items = []
  actions = []

  # Cabeçalho Informativo
  mode_label = (
      "Foco"
      if mode == "work"
      else ("Pausa Curta" if mode == "short_break" else "Pausa Longa")
  )
  st_label = (
      "Executando"
      if st == "running"
      else ("Pausado" if st == "paused" else "Parado")
  )
  status_header = (
      f"<b><span foreground='#bd93f9'>[POMODORO]</span></b>  Estado: <span"
      f" foreground='#50fa7b'>{st_label}</span> ({mode_label}) | Ciclos"
      f" Concluídos: <span foreground='#ff79c6'>{cycles}</span>"
  )
  menu_items.append(status_header)
  actions.append(None)

  menu_items.append(
      "<span foreground='#6272a4'>─────────────────────────────────────────────────────────</span>"
  )
  actions.append(None)

  # Ações rápidas dependendo do estado
  if st == "running":
    menu_items.append("  <span foreground='#f1fa8c'>󰏤</span> <b>Pausar Cronômetro</b>")
    actions.append(["pause"])
  elif st == "paused":
    menu_items.append("  <span foreground='#50fa7b'>󰐊</span> <b>Retomar Cronômetro</b>")
    actions.append(["resume"])

  # Opções de início de ciclo
  menu_items.append(
      "  <span foreground='#ff5555'>󰄉</span> <b>Iniciar Foco (90 min)</b>"
  )
  actions.append(["start", "90", "work"])

  menu_items.append(
      "  <span foreground='#50fa7b'>󰅶</span> <b>Iniciar Pausa (30 min)</b>"
  )
  actions.append(["start", "30", "short_break"])

  menu_items.append(
      "  <span foreground='#8be9fd'>󰒲</span> <b>Iniciar Pausa Rápida (10 min)</b>"
  )
  actions.append(["start", "10", "short_break"])

  menu_items.append(
      "  <span foreground='#bd93f9'>󰥔</span> <b>Tempo Personalizado...</b>"
  )
  actions.append("custom")

  if st in ("running", "paused"):
    menu_items.append(
        "  <span foreground='#ff79c6'>󰑮</span> <b>Pular para Próximo Ciclo</b>"
    )
    actions.append(["skip"])

    menu_items.append(
        "  <span foreground='#ff5555'>󰓛</span> <b>Resetar / Parar Cronômetro</b>"
    )
    actions.append(["stop"])

  menu_input = "\n".join(menu_items)

  rofi_cmd = [
      "rofi",
      "-dmenu",
      "-i",
      "-markup-rows",
      "-format",
      "i",
      "-p",
      "🍅 Pomodoro",
      "-theme-str",
      """
        window { 
            width: 45%; 
        }
        listview { 
            lines: 9; 
            columns: 1; 
            spacing: 3px;
        }
        element { 
            padding: 6px 12px; 
            border-radius: 4px;
        }
        entry { 
            placeholder: "Selecione uma ação do Pomodoro..."; 
        }
      """,
  ]

  res = subprocess.run(
      rofi_cmd, input=menu_input, text=True, capture_output=True
  )

  if res.returncode == 0 and res.stdout.strip().isdigit():
    idx = int(res.stdout.strip())
    action = actions[idx]
    if action == "custom":
      mins = ask_custom_time()
      if mins:
        run_pomodoro(["start", str(mins), "work"])
    elif isinstance(action, list):
      run_pomodoro(action)


if __name__ == "__main__":
  main()
