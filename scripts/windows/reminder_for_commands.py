#!/usr/bin/env python3
import os
import re
import subprocess
import sys
from pathlib import Path

# Localização do arquivo de anotações
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

    # Linhas vazias
    if not line:
      i += 1
      continue

    # Qualquer linha que não seja comentário é tratada como comando
    cmd = line
    desc = current_desc if current_desc else "(sem descrição)"
    entries.append((current_cat, desc, cmd))

    current_desc = ""
    i += 1

  return entries


def main():
  if not COMMANDS_FILE.is_file():
    subprocess.run(
        ["notify-send", "Erro", f"Arquivo não encontrado: {COMMANDS_FILE}"]
    )
    sys.exit(1)

  entries = parse_commands(COMMANDS_FILE)

  if not entries:
    sys.exit(0)

  # Calcula automaticamente a maior categoria e a maior descrição da lista
  max_cat = max(len(cat) for cat, _, _ in entries)
  max_desc = max(len(desc) for _, desc, _ in entries)

  # Define larguras mínimas de respiro estético
  cat_width = max(max_cat, 16)
  desc_width = max(max_desc, 30)

  # Formata com largura dinâmica: o '│' fica sempre na mesma coluna vertical
  formatted_rows = [
      f"{cat:<{cat_width}} │ {desc:<{desc_width}} │ {cmd}"
      for cat, desc, cmd in entries
  ]
  menu_input = "\n".join(formatted_rows)

  rofi_cmd = [
      "rofi",
      "-dmenu",
      "-i",
      "-format",
      "i",
      "-p",
      "⚡ Comandos",
      "-theme-str",
      """
        window { width: 85%; }
        listview { lines: 18; columns: 1; }
        entry { placeholder: "Buscar comando por categoria, ação ou sintaxe..."; }
      """,
  ]

  res = subprocess.run(
      rofi_cmd, input=menu_input, text=True, capture_output=True
  )

  if res.returncode == 0 and res.stdout.strip().isdigit():
    idx = int(res.stdout.strip())
    selected_cmd = entries[idx][2]

    subprocess.run(
        ["xclip", "-selection", "clipboard"],
        input=selected_cmd.encode("utf-8"),
    )

    subprocess.run(
        ["notify-send", "Comando copiado!", selected_cmd, "-t", "3000"]
    )


if __name__ == "__main__":
  main()