#!/usr/bin/env python3
import os
from pathlib import Path
import re
import subprocess
import sys

COMMANDS_FILE = Path.home() / "dotfiles" / "others" / "commands.txt"


def parse_commands(file_path: Path):
  entries = []
  current_cat = "GERAL"
  current_desc = ""

  with open(file_path, "r", encoding="utf-8", errors="replace") as f:
    lines = f.readlines()

  i = 0
  n = len(lines)

  while i < n:
    raw_line = lines[i].rstrip("\r\n")
    line = raw_line.strip()

    # Detecta cabeçalhos de categoria (# -----)
    if re.match(r"^#\s*-{3,}", line):
      i += 1
      if i < n:
        cat_candidate = lines[i].strip().lstrip("#").strip()
        if cat_candidate and not re.match(r"^-{3,}", cat_candidate):
          current_cat = cat_candidate
          i += 1
          if i < n and re.match(r"^#\s*-{3,}", lines[i].strip()):
            i += 1
      current_desc = ""
      continue

    # Detecta a descrição (# Descrição)
    if line.startswith("#"):
      desc = line.lstrip("#").strip()
      if desc and not re.match(r"^-+$", desc):
        current_desc = desc
      i += 1
      continue

    if not line:
      i += 1
      continue

    # Linha do comando
    cmd = line
    desc = current_desc if current_desc else "(sem descrição)"
    entries.append((current_cat, desc, cmd))

    current_desc = ""
    i += 1

  return entries


def escape_pango(text: str) -> str:
  return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def main():
  if not COMMANDS_FILE.is_file():
    subprocess.run(
        ["notify-send", "Erro", f"Arquivo não encontrado: {COMMANDS_FILE}"]
    )
    sys.exit(1)

  entries = parse_commands(COMMANDS_FILE)
  if not entries:
    sys.exit(0)

  formatted_rows = []
  commands_map = []

  # Gera duas linhas nativas no Rofi para cada entrada
  for cat, desc, cmd in entries:
    c = escape_pango(cat)
    d = escape_pango(desc)
    k = escape_pango(cmd)

    # Linha 1: Descrição
    formatted_rows.append(
        f"<b><span foreground='#7dcfff'>[{c}]</span>  {d}</b>"
    )
    commands_map.append(cmd)

    # Linha 2: Comando indentado com quase a largura total da tela
    formatted_rows.append(f"<span foreground='#9ece6a'>       ↳  {k}</span>")
    commands_map.append(cmd)

  menu_input = "\n".join(formatted_rows)

  rofi_cmd = [
      "rofi",
      "-dmenu",
      "-i",
      "-markup-rows",
      "-format",
      "i",
      "-p",
      "⚡ Comandos",
      "-theme-str",
      """
        window { 
            width: 85%; 
        }
        listview { 
            lines: 14; 
            columns: 1; 
            spacing: 2px;
        }
        element { 
            padding: 5px 12px; 
            border-radius: 4px;
        }
        entry { 
            placeholder: "Buscar comando por categoria, ação ou sintaxe..."; 
        }
      """,
  ]

  res = subprocess.run(
      rofi_cmd, input=menu_input, text=True, capture_output=True
  )

  # Se selecionou qualquer linha (descrição ou comando)
  if res.returncode == 0 and res.stdout.strip().isdigit():
    idx = int(res.stdout.strip())
    selected_cmd = commands_map[idx]

    subprocess.run(
        ["xclip", "-selection", "clipboard"],
        input=selected_cmd.encode("utf-8"),
    )

    subprocess.run(
        ["notify-send", "Comando copiado!", selected_cmd, "-t", "3000"]
    )


if __name__ == "__main__":
  main()