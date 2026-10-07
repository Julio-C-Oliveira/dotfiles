#!/usr/bin/env python3
"""
task_manager.py - Gerenciador de Tarefas (TO-DO) integrado ao Pomodoro
Armazena e manipula tarefas em ~/dotfiles/others/pomodoro_tasks.json
"""

import json
import os
from pathlib import Path
import time

TASKS_FILE = Path.home() / "dotfiles" / "others" / "pomodoro_tasks.json"


def load_tasks() -> list[dict]:
  if not TASKS_FILE.exists():
    return []
  try:
    with open(TASKS_FILE, "r", encoding="utf-8") as f:
      return json.load(f)
  except Exception:
    return []


def save_tasks(tasks: list[dict]) -> None:
  TASKS_FILE.parent.mkdir(parents=True, exist_ok=True)
  tmp_file = TASKS_FILE.with_suffix(".tmp")
  try:
    with open(tmp_file, "w", encoding="utf-8") as f:
      json.dump(tasks, f, indent=2, ensure_ascii=False)
    tmp_file.replace(TASKS_FILE)
  except Exception:
    pass


def add_task(text: str) -> dict:
  tasks = load_tasks()
  next_id = max([t.get("id", 0) for t in tasks], default=0) + 1
  new_task = {
      "id": next_id,
      "text": text.strip(),
      "status": "pending",  # "pending" ou "done"
      "pomodoros": 0,
      "created_at": time.strftime("%Y-%m-%d %H:%M"),
  }
  tasks.append(new_task)
  save_tasks(tasks)
  return new_task


def toggle_task(task_id: int) -> bool:
  tasks = load_tasks()
  for t in tasks:
    if t.get("id") == task_id:
      t["status"] = "done" if t.get("status") == "pending" else "pending"
      save_tasks(tasks)
      return True
  return False


def edit_task(task_id: int, new_text: str) -> bool:
  tasks = load_tasks()
  for t in tasks:
    if t.get("id") == task_id:
      t["text"] = new_text.strip()
      save_tasks(tasks)
      return True
  return False


def delete_task(task_id: int) -> bool:
  tasks = load_tasks()
  new_tasks = [t for t in tasks if t.get("id") != task_id]
  if len(new_tasks) != len(tasks):
    save_tasks(new_tasks)
    return True
  return False


def clear_completed() -> int:
  tasks = load_tasks()
  pending_tasks = [t for t in tasks if t.get("status") == "pending"]
  removed_count = len(tasks) - len(pending_tasks)
  save_tasks(pending_tasks)
  return removed_count


def increment_task_pomodoros(task_id: int) -> None:
  tasks = load_tasks()
  for t in tasks:
    if t.get("id") == task_id:
      t["pomodoros"] = t.get("pomodoros", 0) + 1
      save_tasks(tasks)
      return
