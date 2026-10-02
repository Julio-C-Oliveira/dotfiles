# Drift Analysis Report - Animated Lockscreen (xsecurelock)

**Date**: 2026-10-02  
**Target Feature**: Animated Lock Screen (`xsecurelock` + `mpv` / Bad Apple)  
**Status**: ⚠️ DRIFT DETECTADO (Arquivos locais em `~/.local/bin` ausentes no repositório)

---

## 1. Contexto & Verificação dos Atalhos (`sxhkdrc`)

Conforme solicitado, verificamos os atalhos do `sxhkd` para a tela de bloqueio.
* **Arquivo no repositório**: `sxhkd/.config/sxhkd/sxhkdrc` (Linhas 149-155)
* **Atalhos Configurados**:
  ```sxhkdrc
  # Lock Screen (Mudo)
  super + alt + q
  	$HOME/.local/bin/lock.sh

  # Lock Screen (Com Áudio)
  super + alt + shift + q
  	$HOME/.local/bin/lock.sh audio
  ```
* **Conclusão para Atalhos**: 🟢 **OK**. Os atalhos no `sxhkdrc` já estão apontando para `$HOME/.local/bin/lock.sh`.

---

## 2. Drift Identificado (Sistema Ativo vs Repositório)

### 🆕 Scripts Ausentes no Repositório (`Import Candidates`):
1. **`~/.local/bin/lock.sh`**:
   - Desliga o `picom` temporariamente, define `XSECURELOCK_SAVER="$HOME/.local/bin/bad_apple_saver"`, executa `xsecurelock` e religa o `picom` após desbloqueio.
2. **`~/.local/bin/bad_apple_saver`**:
   - Executa o `mpv` na janela do saver (`--wid="$XSCREENSAVER_WINDOW"`) reproduzindo o vídeo `"$HOME/downloads/bad_apple_pv.mkv"`.

### 📦 Pacotes no `packages.json`:
1. **`xsecurelock`**: Ausente no `packages.json` (necessário adicionar em `pacman_packages` ou `yay_packages`).
2. **`betterlockscreen`**: Ainda cadastrado em `yay_packages.tools` e `packages_to_setup` (obsoleto, substituído pelo `xsecurelock`).
3. **`mpv`**: 🟢 **OK** (Já registrado em `pacman_packages.multimedia`).

---

## 3. Plano de Importação e Sincronização Proposto

1. **Importar os scripts para o repositório**:
   - Criar a estrutura em `scripts/lock/` (ou módulo de scripts) contendo `lock.sh` e `bad_apple_saver`.
   - Adicionar rotina no script de instalação para vincular/copiar esses executáveis para `~/.local/bin/`.
2. **Atualizar `packages.json`**:
   - Adicionar `xsecurelock` à lista de pacotes.
   - Remover/substituir a entrada legada de setup do `betterlockscreen`.
