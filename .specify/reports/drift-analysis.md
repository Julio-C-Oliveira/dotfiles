# Drift Analysis Report - Plymouth & GRUB

**Date**: 2026-10-02
**Target Modules**: `plymouth` (Boot Splash), GRUB & Initramfs Configuration
**Status**: 🟢 RESOLVIDO (Configurações do repositório sincronizadas)

---

## 1. Summary of Findings & Resolution

A non-destructive comparison was conducted between the live system configurations (`/usr/share/plymouth/themes/umamusume`, `/etc/default/grub`, `/etc/mkinitcpio.conf`) and the dotfiles repository (`plymouth/umamusume/`).

### Status das Ações Realizadas:
1. **`umamusume.plymouth`**: Atualizado no repositório para apontar `ImageDir=/usr/share/plymouth/themes/umamusume`.
2. **`umamusume.script`**: Atualizado no repositório com o script funcional do sistema (sintaxe Plymouth nativa, laço `while`, 74 frames PNG, callback de renderização).
3. **`.gitignore`**: Mantido e atualizado em `plymouth/umamusume/.gitignore` para ignorar `*.png`, `*.jpg` e `frames/`.
4. **Frames Legados (`frames/`)**: A pasta legada `plymouth/umamusume/frames/` com arquivos JPG obsoletos foi removida do repositório.

---

## 2. Tarefa Registrada: Download dos Frames do Plymouth (Google Drive)

Conforme a orientação do usuário:
* **Estratégia de Assets**: Os 74 frames PNG do Plymouth serão hospedados externamente no Google Drive para não inflar o tamanho do repositório Git.
* **Tarefa a Implementar**: Adicionar uma rotina no script de instalação (`scripts/installation_script/utils.py`) chamada `unpack_plymouth_theme()` (ou similar a `unpack_wallpapers()`) para baixar/descompactar os frames do Drive em `/usr/share/plymouth/themes/umamusume/` durante o setup do sistema.

---

## 3. Recomendações de Bootloader (GRUB & Initramfs)

Para garantir que o tema Plymouth `umamusume` funcione em novas instalações:
1. **`/etc/default/grub`**: Incluir `quiet splash` na variável `GRUB_CMDLINE_LINUX_DEFAULT`.
2. **`/etc/mkinitcpio.conf`**: Incluir o hook `plymouth` na lista `HOOKS=(base udev plymouth ...)`.
3. Executar `sudo mkinitcpio -P` e `sudo grub-mkconfig -o /boot/grub/grub.cfg` no final da instalação.
