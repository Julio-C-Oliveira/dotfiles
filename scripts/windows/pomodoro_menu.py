#!/usr/bin/env python3
"""
pomodoro_menu.py - Menu Rofi para Controle do Pomodoro & TO-DO List
Integração de ciclo de foco/pausa com gerenciamento de tarefas e descrições.
"""

import html
import json
from pathlib import Path
import shutil
import subprocess
import sys
import textwrap

sys.path.insert(0, str(Path(__file__).parent.parent))
try:
  import task_manager
except Exception:
  task_manager = None

POMODORO_SCRIPT = Path.home() / "dotfiles" / "scripts" / "pomodoro.py"
STATE_FILE = Path("/tmp/pomodoro_state.json")


def escape_pango(text: str) -> str:
  return html.escape(str(text))


def notify_user(title: str, msg: str, urgency: str = "normal") -> None:
  if shutil.which("notify-send"):
    try:
      subprocess.Popen([
          "notify-send",
          "-a", "Pomodoro",
          "-u", urgency,
          "-i", "alarm-clock",
          title,
          msg,
      ])
    except Exception:
      pass


def copy_to_clipboard(text: str) -> bool:
  for clip_cmd in [
      ["xclip", "-selection", "clipboard"],
      ["xsel", "--clipboard", "--input"],
      ["wl-copy"],
  ]:
    if shutil.which(clip_cmd[0]):
      try:
        subprocess.run(
            clip_cmd,
            input=text.encode("utf-8"),
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return True
      except Exception:
        continue
  return False


def format_description_rows(desc: str, max_width: int = 65) -> list[str]:
  if not desc or not desc.strip():
    return [
        "<b><span foreground='#6272a4'>[DESCRIÇÃO]</span></b>  <span foreground='#6272a4'><i>(Sem descrição cadastrada)</i></span>"
    ]

  raw_paragraphs = desc.strip().splitlines()
  wrapped_lines: list[str] = []
  for p in raw_paragraphs:
    p_clean = p.strip()
    if not p_clean:
      continue
    chunks = textwrap.wrap(p_clean, width=max_width)
    wrapped_lines.extend(chunks if chunks else [p_clean])

  if not wrapped_lines:
    return [
        "<b><span foreground='#6272a4'>[DESCRIÇÃO]</span></b>  <span foreground='#6272a4'><i>(Sem descrição cadastrada)</i></span>"
    ]

  rows: list[str] = []
  prefix_first = "<b><span foreground='#8be9fd'>[DESCRIÇÃO]</span></b>  "
  prefix_indent = "               "
  for i, line in enumerate(wrapped_lines):
    prefix = prefix_first if i == 0 else prefix_indent
    rows.append(f"{prefix}<span foreground='#f8f8f2'>{escape_pango(line)}</span>")
  return rows


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


def ask_text_input(
    prompt: str,
    placeholder: str = "",
    initial_text: str = "",
    allow_empty: bool = False,
) -> str | None:
  clean_placeholder = placeholder.replace('"', '\\"').replace("\n", " ")
  rofi_cmd = [
      "rofi",
      "-dmenu",
      "-p",
      prompt,
  ]
  if initial_text:
    rofi_cmd.extend(["-filter", initial_text])

  rofi_cmd.extend([
      "-theme-str",
      f"""
        window {{ width: 50%; }}
        listview {{ lines: 0; }}
        entry {{ placeholder: "{clean_placeholder}"; }}
      """,
  ])
  res = subprocess.run(rofi_cmd, capture_output=True, text=True)
  if res.returncode == 0:
    val = res.stdout.strip()
    if val or allow_empty:
      return val
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
  """Exibe submenu de ações e descrição para uma tarefa específica."""
  t_id = task["id"]

  while True:
    current_task = None
    if task_manager:
      current_task = task_manager.get_task(t_id)
    if not current_task:
      current_task = task

    t_text = escape_pango(current_task["text"])
    t_status = current_task.get("status", "pending")
    pomos = current_task.get("pomodoros", 0)
    desc = current_task.get("description", "").strip()

    options = []
    actions = []

    # Cabeçalho da Tarefa
    options.append(
        f"<b><span foreground='#bd93f9'>[TAREFA]</span></b>     <span foreground='#f8f8f2'>{t_text}</span> <span foreground='#6272a4'>({pomos} ciclos)</span>"
    )
    actions.append("edit_title")

    # Linhas da Descrição
    desc_rows = format_description_rows(desc, max_width=65)
    for row in desc_rows:
      options.append(row)
      actions.append("edit_desc")

    options.append("<span foreground='#6272a4'>─────────────────────────────────────────────────────────</span>")
    actions.append(None)

    first_action_idx = len(options)

    if t_status == "pending":
      options.append("  <span foreground='#50fa7b'>🚀</span> <b>Iniciar Foco (90 min) nesta tarefa</b>")
      actions.append("start_focus")

      options.append("  <span foreground='#8be9fd'>✔️</span> <b>Marcar como Concluída</b>")
      actions.append("toggle_status")
    else:
      options.append("  <span foreground='#f1fa8c'>↩️</span> <b>Reabrir Tarefa (Marcar como Pendente)</b>")
      actions.append("toggle_status")

    options.append("  <span foreground='#f1fa8c'>✏️</span> <b>Editar Título</b>")
    actions.append("edit_title")

    desc_label = "Editar Descrição" if desc else "Adicionar Descrição"
    desc_icon = "✏️" if desc else "➕"
    options.append(f"  <span foreground='#bd93f9'>{desc_icon}</span> <b>{desc_label}</b>")
    actions.append("edit_desc")

    if desc:
      options.append("  <span foreground='#8be9fd'>📋</span> <b>Copiar Descrição</b>")
      actions.append("copy_desc")

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
        "Detalhes da Tarefa",
        "-selected-row",
        str(first_action_idx),
        "-theme-str",
        f"""
          window {{ width: 60%; }}
          listview {{ lines: {min(14, len(options))}; spacing: 3px; }}
          element {{ padding: 6px 12px; border-radius: 4px; }}
        """,
    ]

    res = subprocess.run(rofi_cmd, input=menu_input, text=True, capture_output=True)
    if res.returncode != 0 or not res.stdout.strip().isdigit():
      # Usuário pressionou Esc
      return "stay"

    idx = int(res.stdout.strip())
    if idx >= len(actions):
      return "stay"

    action = actions[idx]

    if action == "start_focus":
      run_pomodoro(["start", "90", "work", str(t_id), current_task["text"]])
      return "exit"
    elif action == "toggle_status":
      if task_manager:
        task_manager.toggle_task(t_id)
      return "stay"
    elif action == "edit_title":
      new_title = ask_text_input(
          "Novo título:",
          placeholder="Digite o novo título...",
          initial_text=current_task["text"],
      )
      if new_title and task_manager:
        task_manager.edit_task(t_id, new_text=new_title)
        task["text"] = new_title
      continue
    elif action == "edit_desc":
      new_desc = ask_text_input(
          "Nova descrição:",
          placeholder="Digite a descrição (ou deixe vazio para remover)...",
          initial_text=current_task.get("description", ""),
          allow_empty=True,
      )
      if new_desc is not None and task_manager:
        task_manager.edit_task_description(t_id, new_desc)
        task["description"] = new_desc
      continue
    elif action == "copy_desc":
      if desc:
        copy_to_clipboard(desc)
        notify_user("📋 Pomodoro", "Descrição copiada para a área de transferência!", "low")
      continue
    elif action == "delete":
      if task_manager:
        task_manager.delete_task(t_id)
      return "stay"
    elif action == "back" or action is None:
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
      has_desc = bool(t.get("description", "").strip())
      desc_icon = " <span foreground='#8be9fd'>󰈙</span>" if has_desc else ""
      line = (
          f"  <span foreground='#f8f8f2'>󰄱</span>  <b>{t_text}</b>{active_badge}{desc_icon}"
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
        has_desc = bool(t.get("description", "").strip())
        desc_icon = " <span foreground='#6272a4'>󰈙</span>" if has_desc else ""
        line = (
            f"  <span foreground='#6272a4'>󰄵  <s>{t_text}</s>{desc_icon}"
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
      new_title = ask_text_input(
          "📝 Nova Tarefa:",
          placeholder="Digite o título da tarefa...",
      )
      if new_title and task_manager:
        new_desc = ask_text_input(
            "📄 Descrição (opcional):",
            placeholder="Digite a descrição (Enter para pular, Esc para cancelar)...",
            allow_empty=True,
        )
        if new_desc is not None:
          task_manager.add_task(new_title, new_desc)
    elif action_type == "task_click":
      result = task_action_menu(action_val)
      if result == "exit":
        break
    elif action_type == "clear_done":
      if task_manager:
        task_manager.clear_completed()


if __name__ == "__main__":
  main()
