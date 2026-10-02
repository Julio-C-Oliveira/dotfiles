<!--
Sync Impact Report
------------------
Version Change: N/A -> 1.0.0
Ratification Date: 2026-10-02
Modified Principles: N/A (Initial ratification)
Added Principles:
  - I. Espelhamento Obrigatório de Pacotes
  - II. Automação e Instalador Completo
  - III. Isolamento Root/Stow
  - IV. Idempotência Continuada
  - V. Proibição Absoluta de Segredos (NON-NEGOTIABLE)
  - VI. Higiene de Artefatos & Ignore Policy
Added Sections:
  - Arquitetura do Sistema & Suporte Multi-Distro
  - Workflow de Instalação, Teste & Manutenção
  - Governance
Follow-up TODOs: None
-->

# Dotfiles Workstation Governance Constitution

## Core Principles

### I. Espelhamento Obrigatório de Pacotes
Nenhuma configuração de aplicação pode ser adicionada ao repositório sem que o respectivo pacote base seja explicitamente adicionado à lista de pacotes mantida e suportado pelo fluxo de instalação.

### II. Automação e Instalador Completo
Toda configuração entrevistada ou privilegiada (`/etc/`, `/usr/share/`, hooks de sistema ou regras PAM/polkit) DEVE ter uma rotina de automação explícita nos scripts de instalação. A mera existência de diretórios no repositório sem rotina de instalação correspondente é estritamente proibida.

### III. Isolamento Root/Stow
Configurações de usuário (`$HOME` / `~/.config`) DEVEM ser geridas EXCLUSIVAMENTE por GNU Stow ou symlinks de usuário. Configurações que exigem privilégios elevados pertencem EXCLUSIVAMENTE ao script de instalação com elevação explícita via `sudo`. NUNCA misturar escopos de permissão ou rotinas de vinculação.

### IV. Idempotência Continuada
Todos os scripts de instalação e funções de manutenção DEVEM ser seguros para reexecuções consecutivas e incondicionais. Operações devem utilizar flags idempotentes (`--needed`), checagens prévias de existência de arquivos/links e validações via `shutil.which()`.

### V. Proibição Absoluta de Segredos (NON-NEGOTIABLE)
É estritamente PROIBIDO versionar chaves privadas (SSH/GPG), tokens de API, credenciais, senhas em texto plano ou qualquer informação sensível. Qualquer violação constitui falha de segurança de gravidade CRÍTICA e exige revogação imediata e limpeza do histórico.

### VI. Higiene de Artefatos & Ignore Policy
Arquivos de cache (`__pycache__/`), logs (`install.log`), bancos temporários e estados de runtime DEVEM ser filtrados por `.gitignore` e `.dotfilesignore`. Arquivos binários e grandes arquivos compactados (`.7z`) DEVEM ser avaliados para migração ou download externo via script.

## Arquitetura do Sistema & Suporte Multi-Distro

- **Distribuições Alvo**: Suporte a distribuições Linux (com foco em Gentoo, Arch Linux e Debian/Ubuntu/Fedora).
- **Modularidade de Dotfiles**: Cada aplicação (ex: `bash`, `kitty`, `i3`, `bspwm`, `rofi`, `yazi`, `picom`, `plymouth`, `sddm`) possui diretório dedicado e estrutura limpa compatível com GNU Stow.
- **Gerenciamento de Pacotes**: Suporte a instalações via gerenciadores de pacotes nativos (`emerge`, `pacman`, `apt`) através de abstrações nos scripts de instalação.

## Workflow de Instalação, Teste & Manutenção

- **Validação Dry-Run**: Alterações no instalador ou adição de novos módulos devem ser testados antes da aplicação completa para prevenir quebras do ambiente ativo.
- **Simetria de Instalação**: Scripts de instalação devem registrar logs de progresso (`install.log` ignorado no versionamento) e tratar falhas graciosamente.
- **Detecção de Drift**: O sistema deve permitir comparar periodicamente as configurações do ambiente ativo (`~/.config`, `/etc`) com o repositório (`/speckit-detect-drift`).

## Governance

- Esta Constituição se sobrepõe a qualquer prática não documentada ou decisão ad-hoc no repositório.
- **Procedimento de Emenda**: Alterações nas regras de governança ou nos princípios exigem atualização da versão constitucional, documentação da justificativa no relatório de impacto de sincronização e atualização das ferramentas de validação do Spec Kit.
- **Políticas de Versionamento Semântico**:
  - **MAJOR (X.0.0)**: Remoção ou redefinição incompatível de princípios não-negociáveis ou regras de governança.
  - **MINOR (0.X.0)**: Adição de novos princípios, seções estruturais ou ampliação de diretrizes.
  - **PATCH (0.0.X)**: Clarificações, correções tipográficas e ajustes de estilo sem alteração semântica.
- **Revisão de Conformidade**: Todos os commits, Pull Requests e automações do Spec Kit DEVEM validar o cumprimento estrito dos Princípios I a VI e das regras de ignore.

---
**Version**: 1.0.0 | **Ratified**: 2026-10-02 | **Last Amended**: 2026-10-02
