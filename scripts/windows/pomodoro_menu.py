#!/usr/bin/env python3
"""
pomodoro_menu.py - Menu Rofi para Controle do Pomodoro & TO-DO List
Integração de ciclo de foco/pausa com gerenciamento de tarefas.
"""

import html
import json
from pathlib import Path
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
try:
  import task_manager
except Exception:
  task_manager = None

POMODORO_SCRIPT = Path.home() / "dotfiles" / "scripts" / "pomodoro.py"
STATE_FILE = Path("/tmp/pomodoro_state.json")


def escape_pango(text: str) -> str:
  return html.escape(str(text))


def load_state() -> dict:
  if STATE_FILE.exists():
    try:
      with open(STATE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)
    except Exception:
      pass
  return {
      "state": "stopped",
      "mode": "work",
      "cycle_count": 0,
      "task_id": None,
      "task_name": "",
  }


def run_pomodoro(args: list[str]):
  subprocess.run([str(POMODORO_SCRIPT)] + args)


def ask_text_input(prompt: str, placeholder: str = "") -> str | None:
  rofi_cmd = [
      "rofi",
      "-dmenu",
      "-p",
      prompt,
      "-theme-str",
      f"""
        window {{ width: 45%; }}
        listview {{ lines: 0; }}
        entry {{ placeholder: "{placeholder}"; }}
      """,
  ]
  res = subprocess.run(rofi_cmd, capture_output=True, text=True)
  if res.returncode == 0 and res.stdout.strip():
    return res.stdout.strip()
  return None


def ask_custom_time() -> float | None:
  val = ask_text_input("⏱️ Minutos:", "Digite a duração em minutos (ex: 45, 60, 90)...")
  if val:
    try:
      mins = float(val)
      if mins > 0:
        return mins
    except ValueError:
      pass
  return None


def task_action_menu(task: dict) -> str:
  """Exibe submenu de ações para uma tarefa específica."""
  t_id = task["id"]
  t_text = escape_pango(task["text"])
  t_status = task.get("status", "pending")
  pomos = task.get("pomodoros", 0)

  options = []
  actions = []

  options.append(
      f"<b><span foreground='#bd93f9'>[TAREFA]</span></b>  <span foreground='#f8f8f2'>{t_text}</span> <span foreground='#6272a4'>({pomos} ciclos)</span>"
  )
  actions.append(None)

  options.append("<span foreground='#6272a4'>─────────────────────────────────────────────────────────</span>")
  actions.append(None)

  if t_status == "pending":
    options.append("  <span foreground='#50fa7b'>🚀</span> <b>Iniciar Foco (90 min) nesta tarefa</b>")
    actions.append("start_focus")

    options.append("  <span foreground='#8be9fd'>✔️</span> <b>Marcar como Concluída</b>")
    actions.append("toggle_status")

    options.append("  <span foreground='#f1fa8c'>✏️</span> <b>Editar Título</b>")
    actions.append("edit")
  else:
    options.append("  <span foreground='#f1fa8c'>↩️</span> <b>Reabrir Tarefa (Marcar como Pendente)</b>")
    actions.append("toggle_status")

  options.append("  <span foreground='#ff5555'>🗑️</span> <b>Excluir Tarefa</b>")
  actions.append("delete")

  options.append("  <span foreground='#6272a4'>🔙</span> <b>Voltar</b>")
  actions.append("back")

  menu_input = "\n".join(options)

  rofi_cmd = [
      "rofi",
      "-dmenu",
      "-i",
      "-markup-rows",
      "-format",
      "i",
      "-p",
      "Opções da Tarefa",
      "-theme-str",
      """
        window { width: 50%; }
        listview { lines: 7; spacing: 3px; }
        element { padding: 6px 12px; border-radius: 4px; }
      """,
  ]

  res = subprocess.run(rofi_cmd, input=menu_input, text=True, capture_output=True)
  if res.returncode == 0 and res.stdout.strip().isdigit():
    idx = int(res.stdout.strip())
    action = actions[idx]
    if action == "start_focus":
      run_pomodoro(["start", "90", "work", str(t_id), task["text"]])
      return "exit"
    elif action == "toggle_status":
      if task_manager:
        task_manager.toggle_task(t_id)
    elif action == "edit":
      new_title = ask_text_input("Novo título:", task["text"])
      if new_title and task_manager:
        task_manager.edit_task(t_id, new_title)
    elif action == "delete":
      if task_manager:
        task_manager.delete_task(t_id)
  return "stay"


def main():
  while True:
    state = load_state()
    st = state.get("state", "stopped")
    mode = state.get("mode", "work")
    cycles = state.get("cycle_count", 0)
    curr_task_id = state.get("task_id")
    curr_task_name = state.get("task_name", "")

    tasks = task_manager.load_tasks() if task_manager else []
    pending_tasks = [t for t in tasks if t.get("status") == "pending"]
    done_tasks = [t for t in tasks if t.get("status") == "done"]

    menu_items = []
    actions = []

    # 1. Cabeçalho Informativo
    mode_label = (
        "Foco"
        if mode == "work"
        else ("Pausa" if mode == "short_break" else "Pausa Longa")
    )
    st_label = (
        "Executando"
        if st == "running"
        else ("Pausado" if st == "paused" else "Parado")
    )
    status_header = (
        f"<b><span foreground='#bd93f9'>[POMODORO]</span></b>  Estado: <span"
        f" foreground='#50fa7b'>{st_label}</span> ({mode_label}) | Ciclos"
        f" Hoje: <span foreground='#ff79c6'>{cycles}</span>"
    )
    if curr_task_name and st in ("running", "paused"):
      status_header += f" | Foco: <span foreground='#50fa7b'>{escape_pango(curr_task_name)}</span>"

    menu_items.append(status_header)
    actions.append(None)

    menu_items.append(
        "<span foreground='#6272a4'>─────────────────────────────────────────────────────────</span>"
    )
    actions.append(None)

    # 2. Controles do Cronômetro
    if st == "running":
      menu_items.append("  <span foreground='#f1fa8c'>󰏤</span> <b>Pausar Cronômetro</b>")
      actions.append(("timer", ["pause"]))
      menu_items.append("  <span foreground='#ff79c6'>󰑮</span> <b>Pular para Próximo Ciclo</b>")
      actions.append(("timer", ["skip"]))
      menu_items.append("  <span foreground='#ff5555'>󰓛</span> <b>Resetar / Parar Cronômetro</b>")
      actions.append(("timer", ["stop"]))
    elif st == "paused":
      menu_items.append("  <span foreground='#50fa7b'>󰐊</span> <b>Retomar Cronômetro</b>")
      actions.append(("timer", ["resume"]))
      menu_items.append("  <span foreground='#ff79c6'>󰑮</span> <b>Pular para Próximo Ciclo</b>")
      actions.append(("timer", ["skip"]))
      menu_items.append("  <span foreground='#ff5555'>󰓛</span> <b>Resetar / Parar Cronômetro</b>")
      actions.append(("timer", ["stop"]))
    else:
      menu_items.append("  <span foreground='#ff5555'>󰄉</span> <b>Iniciar Foco Geral (90 min)</b>")
      actions.append(("timer", ["start", "90", "work"]))
      menu_items.append("  <span foreground='#50fa7b'>󰅶</span> <b>Iniciar Pausa (30 min)</b>")
      actions.append(("timer", ["start", "30", "short_break"]))
      menu_items.append("  <span foreground='#8be9fd'>󰒲</span> <b>Iniciar Pausa Rápida (10 min)</b>")
      actions.append(("timer", ["start", "10", "short_break"]))
      menu_items.append("  <span foreground='#bd93f9'>󰥔</span> <b>Tempo Personalizado...</b>")
      actions.append(("custom_timer", None))

    # 3. Seção TO-DO (Tarefas Pendentes)
    menu_items.append(
        "<span foreground='#6272a4'>── TAREFAS PENDENTES ────────────────────────────────────</span>"
    )
    actions.append(None)

    menu_items.append("  <span foreground='#50fa7b'>➕</span> <b>Adicionar Nova Tarefa...</b>")
    actions.append(("add_task", None))

    for t in pending_tasks:
      t_text = escape_pango(t["text"])
      pomos = t.get("pomodoros", 0)
      pomo_str = f"{pomos} ciclos" if pomos != 1 else "1 ciclo"
      is_active = (curr_task_id == t["id"] and st in ("running", "paused"))
      active_badge = " <span foreground='#50fa7b'>[🎯 Ativa]</span>" if is_active else ""
      line = (
          f"  <span foreground='#f8f8f2'>󰄱</span>  <b>{t_text}</b>{active_badge}"
          f"  <span foreground='#bd93f9'>[{pomo_str}]</span>"
      )
      menu_items.append(line)
      actions.append(("task_click", t))

    if not pending_tasks:
      menu_items.append("  <span foreground='#6272a4'><i>(Nenhuma tarefa pendente)</i></span>")
      actions.append(None)

    # 4. Seção de Concluídas
    if done_tasks:
      menu_items.append(
          f"<span foreground='#6272a4'>── TAREFAS CONCLUÍDAS ({len(done_tasks)}) ─────────────────────────</span>"
      )
      actions.append(None)

      for t in done_tasks:
        t_text = escape_pango(t["text"])
        pomos = t.get("pomodoros", 0)
        pomo_str = f"{pomos} ciclos" if pomos != 1 else "1 ciclo"
        line = (
            f"  <span foreground='#6272a4'>󰄵  <s>{t_text}</s>"
            f"  [{pomo_str}]</span>"
        )
        menu_items.append(line)
        actions.append(("task_click", t))

      menu_items.append("  <span foreground='#ff5555'>🗑️</span> <span foreground='#ff5555'>Limpar todas as tarefas concluídas</span>")
      actions.append(("clear_done", None))

    menu_input = "\n".join(menu_items)

    rofi_cmd = [
        "rofi",
        "-dmenu",
        "-i",
        "-markup-rows",
        "-format",
        "i",
        "-p",
        "🍅 Pomodoro & Tarefas",
        "-theme-str",
        """
          window { 
              width: 55%; 
          }
          listview { 
              lines: 15; 
              columns: 1; 
              spacing: 3px;
          }
          element { 
              padding: 5px 12px; 
              border-radius: 4px;
          }
          entry { 
              placeholder: "Selecione uma ação, adicione tarefas ou escolha em qual focar..."; 
          }
        """,
    ]

    res = subprocess.run(rofi_cmd, input=menu_input, text=True, capture_output=True)

    if res.returncode != 0 or not res.stdout.strip().isdigit():
      # Usuário pressionou Esc
      break

    idx = int(res.stdout.strip())
    action_info = actions[idx] if idx < len(actions) else None
    if not action_info:
      continue

    action_type, action_val = action_info

    if action_type == "timer":
      run_pomodoro(action_val)
      break
    elif action_type == "custom_timer":
      mins = ask_custom_time()
      if mins:
        run_pomodoro(["start", str(mins), "work"])
        break
    elif action_type == "add_task":
      new_title = ask_text_input("📝 Nova Tarefa:", "Digite a descrição da tarefa...")
      if new_title and task_manager:
        task_manager.add_task(new_title)
    elif action_type == "task_click":
      result = task_action_menu(action_val)
      if result == "exit":
        break
    elif action_type == "clear_done":
      if task_manager:
        task_manager.clear_completed()


if __name__ == "__main__":
  main()
