#!/usr/bin/env python3
import os
import re
import subprocess
import sys
from pathlib import Path


def get_sxhkdrc_path() -> Path:
  config_home = os.environ.get("XDG_CONFIG_HOME")
  if config_home:
    return Path(config_home) / "sxhkd" / "sxhkdrc"
  return Path.home() / ".config" / "sxhkd" / "sxhkdrc"


def parse_sxhkdrc(file_path: Path):
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

    # 1. Detecta cabeçalhos de bloco (# -----)
    if re.match(r"^#\s*-{3,}", line):
      i += 1
      # Captura o nome da categoria no meio das divisórias
      if i < n:
        cat_candidate = lines[i].strip().lstrip("#").strip()
        # Se não for outra linha de traços, é a categoria
        if cat_candidate and not re.match(r"^-{3,}", cat_candidate):
          current_cat = cat_candidate
          i += 1
          # Pula o traço de fechamento (# -----) se existir
          if i < n and re.match(r"^#\s*-{3,}", lines[i].strip()):
            i += 1

      current_desc = ""  # Reseta qualquer descrição ao trocar de categoria
      continue

    # 2. Comentários (descrição do atalho)
    if line.startswith("#"):
      desc = line.lstrip("#").strip()
      # Ignora linhas com apenas '#' vazio ou traços soltos
      if desc and not re.match(r"^-+$", desc):
        current_desc = desc
      i += 1
      continue

    # 3. Linhas vazias
    if not line:
      i += 1
      continue

    # 4. Linhas indentadas (são os comandos executados pelo sxhkd, ignoramos)
    if raw_line.startswith((" ", "\t")):
      i += 1
      continue

    # 5. Se chegou aqui na coluna 0, é a linha do atalho
    key = line
    desc = current_desc if current_desc else "(sem descrição)"
    entries.append((current_cat, key, desc))

    current_desc = ""  # Consome a descrição para não vazar pro próximo atalho
    i += 1

  return entries


def main():
  conf_path = get_sxhkdrc_path()

  if not conf_path.is_file():
    subprocess.run(
        ["notify-send", "Erro", f"sxhkdrc não encontrado em {conf_path}"]
    )
    sys.exit(1)

  entries = parse_sxhkdrc(conf_path)

  # Ajuste de largura: Categoria (24) │ Atalho (38) │ Descrição
  formatted_rows = [
      f"{cat:<24} │ {key:<38} │ {desc}" for cat, key, desc in entries
  ]
  menu_input = "\n".join(formatted_rows)

  rofi_cmd = [
      "rofi",
      "-dmenu",
      "-i",
      "-p",
      "⌨ Atalhos",
      "-theme-str",
      """
        window { width: 75%; }
        listview { lines: 18; columns: 1; }
        entry { placeholder: "Filtrar por categoria, tecla ou comando..."; }
      """,
  ]

  subprocess.run(rofi_cmd, input=menu_input, text=True)


if __name__ == "__main__":
  main()