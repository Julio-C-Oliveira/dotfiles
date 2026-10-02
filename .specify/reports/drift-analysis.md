# Drift Analysis Report - Animated Lockscreen (xsecurelock)

**Date**: 2026-10-02  
**Target Feature**: Animated Lock Screen (`xsecurelock` + `mpv` / Bad Apple)  
**Status**: 🟢 RESOLVIDO (Módulo Stow `xsecurelock` criado e sincronizado)

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
* **Conclusão para Atalhos**: 🟢 **OK**. Os atalhos no `sxhkdrc` apontam corretamente para `$HOME/.local/bin/lock.sh`.

---

## 2. Ações de Sincronização Executadas

### 📁 Módulo Stow `xsecurelock/`
Criada a estrutura em `xsecurelock/.local/bin/`:
1. **`xsecurelock/.local/bin/lock.sh`**: Script wrapper para gerenciar o compositor `picom`, exportar `XSECURELOCK_SAVER` e rodar `xsecurelock`.
2. **`xsecurelock/.local/bin/bad_apple_saver`**: Script do protetor animado usando `mpv` com `--wid="$XSCREENSAVER_WINDOW"`.
3. **Symlinks Ativos**: Aplicado `stow xsecurelock`, vinculando `~/.local/bin/lock.sh` e `~/.local/bin/bad_apple_saver` ao repositório `~/dotfiles/xsecurelock/`.

### 📦 Atualização do `packages.json`
1. **`xsecurelock`**: Adicionado a `arch_packages.window_manager_and_related`.
2. **`stow_packages`**: Adicionado `{"name" : "xsecurelock", "target" : [".local/bin/lock.sh", ".local/bin/bad_apple_saver"]}`.
3. **`betterlockscreen`**: Removido de `yay_packages.tools` e `packages_to_setup`.
