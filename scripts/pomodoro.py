#!/usr/bin/env python3
"""
pomodoro.py - Gerenciador do Pomodoro Integrado
Controle via CLI, módulo para Polybar e integração com Dunst / Sons do Sistema.
"""

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

STATE_FILE = Path("/tmp/pomodoro_state.json")

SOUND_START = "/usr/share/sounds/freedesktop/stereo/bell.oga"
SOUND_END = "/usr/share/sounds/freedesktop/stereo/complete.oga"
SOUND_ALARM = "/usr/share/sounds/freedesktop/stereo/alarm-clock-elapsed.oga"


def play_sound(sound_path: str):
  if not os.path.exists(sound_path):
    return
  player = shutil.which("paplay") or shutil.which("pw-play") or shutil.which("mpv")
  if player:
    cmd = [player, sound_path] if "mpv" not in player else [player, "--no-video", sound_path]
    subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def notify(title: str, msg: str, urgency: str = "normal"):
  if shutil.which("notify-send"):
    subprocess.Popen([
        "notify-send",
        "-a", "Pomodoro",
        "-u", urgency,
        "-i", "alarm-clock",
        title,
        msg,
    ])


def load_state() -> dict:
  default_state = {
      "state": "stopped",  # stopped, running, paused, completed
      "mode": "work",      # work, short_break, long_break
      "end_time": 0.0,
      "duration_sec": 90 * 60,
      "remaining_sec": 90 * 60,
      "cycle_count": 0,
      "completed_at": 0.0,
  }
  if STATE_FILE.exists():
    try:
      with open(STATE_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
        default_state.update(data)
    except Exception:
      pass
  return default_state


def save_state(state: dict):
  tmp_file = STATE_FILE.with_suffix(".tmp")
  try:
    with open(tmp_file, "w", encoding="utf-8") as f:
      json.dump(state, f, indent=2)
    tmp_file.replace(STATE_FILE)
  except Exception:
    pass


def start_cycle(minutes: float, mode: str = "work", manual: bool = True):
  state = load_state()
  duration_sec = int(minutes * 60)
  now = time.time()

  state["state"] = "running"
  state["mode"] = mode
  state["duration_sec"] = duration_sec
  state["remaining_sec"] = duration_sec
  state["end_time"] = now + duration_sec
  state["completed_at"] = 0.0

  save_state(state)
  play_sound(SOUND_START)

  if manual:
    if mode == "work":
      notify("🍅 Foco Iniciado", f"Ciclo de foco de {int(minutes)} minutos iniciado. Bom trabalho!", "normal")
    elif mode in ("short_break", "long_break"):
      notify("☕ Pausa Iniciada", f"Pausa de {int(minutes)} minutos. Relaxe um pouco!", "normal")


def toggle():
  state = load_state()
  st = state.get("state", "stopped")

  if st in ("stopped", "completed"):
    start_cycle(90, "work")
  elif st == "running":
    pause()
  elif st == "paused":
    resume()


def pause():
  state = load_state()
  if state.get("state") == "running":
    now = time.time()
    rem = max(0, int(state.get("end_time", 0) - now))
    state["state"] = "paused"
    state["remaining_sec"] = rem
    save_state(state)
    notify("⏸️ Pomodoro Pausado", f"Cronômetro pausado com {rem // 60:02d}:{rem % 60:02d} restantes.", "low")


def resume():
  state = load_state()
  if state.get("state") == "paused":
    rem = state.get("remaining_sec", 0)
    now = time.time()
    state["state"] = "running"
    state["end_time"] = now + rem
    save_state(state)
    play_sound(SOUND_START)
    notify("▶️ Pomodoro Retomado", f"Ciclo retomado com {rem // 60:02d}:{rem % 60:02d} restantes.", "low")


def stop():
  state = load_state()
  state["state"] = "stopped"
  state["end_time"] = 0.0
  state["remaining_sec"] = state.get("duration_sec", 90 * 60)
  save_state(state)
  notify("⏹️ Pomodoro Resetado", "Cronômetro interrompido e resetado.", "low")


def skip():
  state = load_state()
  curr_mode = state.get("mode", "work")
  cycle_count = state.get("cycle_count", 0)

  if curr_mode == "work":
    cycle_count += 1
    state["cycle_count"] = cycle_count
    save_state(state)
    start_cycle(30, "short_break")
  else:
    start_cycle(90, "work")


def get_status() -> str:
  state = load_state()
  st = state.get("state", "stopped")
  mode = state.get("mode", "work")
  now = time.time()

  # Se está rodando, checa se acabou
  if st == "running":
    end_t = state.get("end_time", 0)
    rem = int(end_t - now)

    if rem <= 0:
      # Concluiu o ciclo
      state["state"] = "completed"
      state["completed_at"] = now
      if mode == "work":
        state["cycle_count"] = state.get("cycle_count", 0) + 1
      save_state(state)

      play_sound(SOUND_END)

      if mode == "work":
        cycles = state["cycle_count"]
        notify(
            "🎉 Ciclo de Foco Finalizado!",
            f"Parabéns! Ciclo #{cycles} (90 min) concluído.\nSugestão: Faça uma pausa de 30 minutos.",
            "critical",
        )
      else:
        notify(
            "☕ Pausa Concluída!",
            "Sua pausa terminou. Pronto para voltar ao foco?",
            "critical",
        )

      return "%{F#50fa7b}🎉 Concluído%{F-}"

    mins = rem // 60
    secs = rem % 60
    time_str = f"{mins:02d}:{secs:02d}"

    if mode == "work":
      return f"%{{F#ff5555}}󰄉%{{F-}} %{{F#f8f8f2}}{time_str}%{{F-}}"
    elif mode == "short_break":
      return f"%{{F#50fa7b}}󰅶%{{F-}} %{{F#f8f8f2}}{time_str}%{{F-}}"
    elif mode == "long_break":
      return f"%{{F#8be9fd}}󰒲%{{F-}} %{{F#f8f8f2}}{time_str}%{{F-}}"

  elif st == "paused":
    rem = state.get("remaining_sec", 0)
    mins = rem // 60
    secs = rem % 60
    time_str = f"{mins:02d}:{secs:02d}"
    return f"%{{F#f1fa8c}}󰏤%{{F-}} %{{F#6272a4}}{time_str}%{{F-}}"

  elif st == "completed":
    completed_at = state.get("completed_at", 0)
    if now - completed_at < 30:
      return "%{F#50fa7b}󰄉 00:00%{F-}"
    else:
      return "%{F#6272a4}󰄉%{F-}"

  # stopped
  return "%{F#6272a4}󰄉%{F-}"


def main():
  if len(sys.argv) < 2:
    print(get_status())
    return

  cmd = sys.argv[1].lower()

  if cmd == "status":
    print(get_status())
  elif cmd == "toggle":
    toggle()
  elif cmd == "pause":
    pause()
  elif cmd == "resume":
    resume()
  elif cmd == "stop" or cmd == "reset":
    stop()
  elif cmd == "skip":
    skip()
  elif cmd == "start":
    minutes = float(sys.argv[2]) if len(sys.argv) > 2 else 90.0
    mode = sys.argv[3] if len(sys.argv) > 3 else "work"
    start_cycle(minutes, mode)
  else:
    print(f"Comando desconhecido: {cmd}", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
  main()
