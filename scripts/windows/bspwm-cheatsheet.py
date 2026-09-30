#!/usr/bin/env python3
import os
from pathlib import Path
import re
import subprocess
import sys


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

    # Detecta cabeçalhos de bloco (# -----)
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

    # Comentários (descrição)
    if line.startswith("#"):
      desc = line.lstrip("#").strip()
      if desc and not re.match(r"^-+$", desc):
        current_desc = desc
      i += 1
      continue

    if not line:
      i += 1
      continue

    # Comandos indentados do sxhkd (ignora)
    if raw_line.startswith((" ", "\t")):
      i += 1
      continue

    # Atalho (coluna 0)
    key = line
    desc = current_desc if current_desc else "(sem descrição)"
    entries.append((current_cat, key, desc))

    current_desc = ""
    i += 1

  return entries


def escape_pango(text: str) -> str:
  return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def main():
  conf_path = get_sxhkdrc_path()

  if not conf_path.is_file():
    subprocess.run(
        ["notify-send", "Erro", f"sxhkdrc não encontrado em {conf_path}"]
    )
    sys.exit(1)

  entries = parse_sxhkdrc(conf_path)
  if not entries:
    sys.exit(0)

  # Mede larguras máximas reais
  max_cat = max(len(cat) for cat, _, _ in entries)
  max_key = max(len(key) for _, key, _ in entries)

  cat_w = max(max_cat, 18)
  key_w = max(max_key, 28)

  formatted_rows = []
  for cat, key, desc in entries:
    padded_cat = f"{cat:<{cat_w}}"
    padded_key = f"{key:<{key_w}}"

    c = escape_pango(padded_cat)
    k = escape_pango(padded_key)
    d = escape_pango(desc)

    # Cores Oficiais Dracula: Roxo (#bd93f9) | Cinza (#6272a4) | Rosa (#ff79c6) | Branco (#f8f8f2)
    row = (
        f"<b><span foreground='#bd93f9'>{c}</span></b> "
        f"<span foreground='#6272a4'>│</span> "
        f"<b><span foreground='#ff79c6'>{k}</span></b> "
        f"<span foreground='#6272a4'>│</span> "
        f"<span foreground='#f8f8f2'>{d}</span>"
    )
    formatted_rows.append(row)

  menu_input = "\n".join(formatted_rows)

  rofi_cmd = [
      "rofi",
      "-dmenu",
      "-i",
      "-markup-rows",
      "-p",
      "⌨ Atalhos",
      "-theme-str",
      """
        window { 
            width: 78%; 
        }
        listview { 
            lines: 16; 
            columns: 1; 
            spacing: 2px;
        }
        element { 
            padding: 4px 8px; 
            border-radius: 0px;
        }
        entry { 
            placeholder: "Filtrar por categoria, tecla ou ação..."; 
        }
      """,
  ]

  subprocess.run(rofi_cmd, input=menu_input, text=True)


if __name__ == "__main__":
  main()