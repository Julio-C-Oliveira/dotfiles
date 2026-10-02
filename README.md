# Repositório de Dotfiles & Gestão de Sistemas

Repositório para armazenar meus dotfiles, configurações do sistema Linux e scripts de automação/instalação.

Este repositório utiliza comandos e workflows assistidos por IA (`.agent/workflows`) para manutenção, especificação de módulos, auditoria e sincronização do sistema.

---

## 🛠️ Fluxo de Trabalho do Agente Spec Kit (Dotfiles)

O fluxo combina a especificação orientada a componentes com auditoria de pacotes, links simbólicos e sincronização com o sistema ativo.

```
                    ┌────────────────────────────────┐
                    │     /speckit-constitution      │ (Regras & Governança)
                    └───────────────┬────────────────┘
                                    │
                    ┌───────────────▼────────────────┐
                    │        /speckit-specify        │ (O que e por quê)
                    └───────────────┬────────────────┘
                                    │
                    ┌───────────────▼────────────────┐
                    │        /speckit-clarify        │ (Dúvidas & Casos de borda)
                    └───────────────┬────────────────┘
                                    │
                    ┌───────────────▼────────────────┐
                    │          /speckit-plan         │ (Arquitetura & Esquemas)
                    └───────────────┬────────────────┘
                                    │
                    ┌───────────────▼────────────────┐
                    │         /speckit-tasks         │ (Checklist atômico)
                    └───────────────┬────────────────┘
                                    │
                    ┌───────────────▼────────────────┐
                    │        /speckit-analyze        │ (Auditoria Spec ↔ Plan ↔ Tasks)
                    └───────────────┬────────────────┘
                                    │
                    ┌───────────────▼────────────────┐
                    │       /speckit-implement       │ (Codificação assistida)
                    └───────────────┬────────────────┘
                                    │
                    ┌───────────────▼────────────────┐
                    │        /speckit-converge       │ (Auditoria Código ↔ Spec)
                    └────────────────────────────────┘
```

---

### 📋 Estágios do Fluxo Principal

| Comando | Função no Domínio de Dotfiles |
| :--- | :--- |
| **`/speckit-constitution`** | Define os 6 princípios não-negociáveis do repositório (Espelhamento de Pacotes, Instalador Completo, Isolamento Root/Stow, Idempotência, Proibição de Segredos e Higiene de Artefatos). |
| **`/speckit-specify`** | Especifica a adição ou alteração de um módulo de dotfiles (ex: Kitty, Bspwm, Zsh, Polybar) ou script de instalação, definindo requisitos funcionais e critérios verificáveis via shell. |
| **`/speckit-clarify`** | Faz perguntas direcionadas para resolver ambiguidades na especificação (escopo Stow vs. root, dependências de hardware/GPU, atalhos sxhkd, etc.). |
| **`/speckit-plan`** | Planeja a estrutura de pastas do módulo, esquemas de configuração (`config-schema.md`), contratos de IPC/atalhos (`contracts/`) e guia de validação de boot (`boot-validation.md`). |
| **`/speckit-tasks`** | Quebra o plano em tarefas atômicas sequenciais e paralelas (`tasks.md`), separadas por módulo, registro de pacotes e rotinas do instalador. |
| **`/speckit-analyze`** | Realiza análise estática e auditoria cruzada (`Spec <-> Plan <-> Tasks`), incluindo a **Fase 0 de Auditoria do Instalador** para checar se todas as pastas têm pacotes e funções no instalador. |
| **`/speckit-implement`** | Executa a implementação das tarefas em `tasks.md`, criando/editando arquivos de configuração, scripts shell/python e validando sintaxe (`bash -n`, `py_compile`). |
| **`/speckit-converge`** | Avalia a base de código contra os artefatos de especificação. Se houver lacunas ou privilégios ausentes no instalador, anexa automaticamente tarefas de convergência ao `tasks.md`. |

---

## 🔒 Portões de Planejamento & Geração de Tarefas

### 1. Plano Prévio Obrigatório (Plan-First Gate)
Para prevenir modificações destrutivas ou não autorizadas no sistema, os seguintes comandos exigem a **apresentação e aprovação de um plano** antes de executar alterações em arquivos ou configurações:
- **`/speckit-constitution`**: Requer aprovação do plano de emenda antes de atualizar a governança.
- **`/speckit-detect-drift`**: Requer aprovação do plano de importação/sincronização antes de copiar arquivos do sistema para o repositório.
- **`/speckit-audit-install`**: Requer aprovação do plano de remediação antes de alterar scripts de instalação (`main.py`, `utils.py`, `packages.json`).
- **`/speckit-implement`**: Requer a existência de um `plan.md` aprovado antes de alterar código ou configurações.
- **`/speckit-converge`**: Requer aprovação prévia se a resolução de gaps exigir alterações arquiteturais profundas.

### 2. Capaz de Gerar/Anexar Tarefas ao `tasks.md`
Além do fluxo derivado de `/speckit-specify` → `/speckit-tasks`, os seguintes comandos estão autorizados a **gerar ou anexar tarefas diretamente ao `tasks.md`**:
- **`/speckit-audit-install`**: Anexa tarefas para criar funções em `utils.py`, registrar pacotes em `packages.json` ou ajustar chamadas em `main.py`.
- **`/speckit-detect-drift`**: Anexa tarefas de importação de pastas em `~/.config` ou sincronização de arquivos modificados.
- **`/speckit-constitution`**: Anexa tarefas de adequação do repositório a novos princípios ratificados.
- **`/speckit-analyze`**: Anexa tarefas de remediação ao identificar incongruências críticas (`INS-*`).
- **`/speckit-converge`**: Anexa tarefas na fase `## Phase N: Convergence` para fechar lacunas identificadas entre a spec e o código.

---

## 🔍 Comandos Específicos para Dotfiles & Manutenção

Além do fluxo principal, o repositório conta com comandos utilitários dedicados ao mapeamento, auditoria e sincronização do sistema Linux:

| Comando | Descrição & Uso |
| :--- | :--- |
| **`/speckit-map`** | **Mapeamento Geral do Repositório**: Gera/atualiza o arquivo de memória [.specify/memory/project-map.md](file:///home/julio/dotfiles/.specify/memory/project-map.md) com o mapa completo de módulos, entrypoints, rotinas do instalador e pacotes, evitando que o agente precise ler todos os arquivos repetidamente. |
| **`/speckit-audit-install`** | **Auditoria do Script de Instalação**: Analisa se o script de instalação (`scripts/installation_script/`) e a lista de pacotes (`packages.json`) estão 100% coerentes e sincronizados com as pastas de dotfiles existentes no repositório. |
| **`/speckit-detect-drift`** | **Detecção de Mudanças Externas**: Compara o ambiente ativo do sistema (`~/.config`, `/etc`, etc.) com os arquivos versionados no repositório, identificando alterações locais não commitadas ou novos aplicativos elegíveis para importação. |
| **`/speckit-ignore`** | **Gerenciamento do `.dotfilesignore`**: Visualiza, testa ou adiciona regras ao arquivo `.dotfilesignore` (ou `.agentignore`), definindo quais arquivos, caches, logs ou segredos o agente deve ignorar durante as varreduras. |

---

## 🛡️ Arquivo de Exclusões (`.dotfilesignore`)

O arquivo [.dotfilesignore](file:///home/julio/dotfiles/.dotfilesignore) garante que o agente ignore e proteja:
- **Segredos e Credenciais**: Chaves SSH (`id_rsa`), certificados (`*.pem`, `*.key`), tokens de nuvem/API.
- **Logs e Caches**: `install.log`, `__pycache__/`, `*.pyc`, diretórios `.cache/`.
- **Dumps Binários**: Compactados grandes (`.7z`, `.iso`, `.tar.gz`) que não devem ir ao Git sem LFS.
- **Estado Temporário**: `.swp`, `Thumbs.db`, `.DS_Store`.

---

## 🚀 Guia de Uso do Script de Instalação (`main.py`)

O script de pós-instalação automatiza a configuração do Arch Linux, pacotes AUR/pacman, aplicação de symlinks via GNU Stow e temas visuais.

### Localização do Script
```bash
python3 scripts/installation_script/main.py [opções]
```

### ⚙️ Opções de Linha de Comando (CLI)

| Flag | Descrição | Valor Padrão |
| :--- | :--- | :--- |
| `-c`, `--config` | Caminho do arquivo JSON com a definição de pacotes. | `packages.json` |
| `-g`, `--gui {sddm,startx}` | Define a interface gráfica/display manager a ser instalada. | Interativo / `sddm` em modo autônomo |
| `-y`, `--yes`, `--non-interactive` | Executa o script de forma 100% não-interativa (sem perguntas manuais). | `False` |
| `--reboot` | Força a reinicialização do sistema ao final da instalação. | `False` |
| `--no-reboot` | Impede a reinicialização automática do sistema ao final. | `False` |
| `--repo-dir` | Caminho do repositório de dotfiles. | Detectado automaticamente |

### 💡 Exemplos de Uso

1. **Modo Interativo Padrão**:
   ```bash
   python3 scripts/installation_script/main.py
   ```
   *Solicitará ao usuário a escolha da GUI (SDDM / startx) e confirmação para reiniciar o sistema.*

2. **Instalação Não-Interativa / Automação Unattended**:
   ```bash
   python3 scripts/installation_script/main.py --non-interactive --gui sddm --no-reboot
   ```
   *Executa sem nenhuma interrupção manual, configura SDDM e finaliza sem reiniciar.*

3. **Especificando Caminho de Repositório Customizado**:
   ```bash
   python3 scripts/installation_script/main.py --repo-dir /caminho/para/dotfiles -y
   ```

### 🛡️ Backup Automático de Conflitos
Ao aplicar os links do GNU Stow, caso existam arquivos ou pastas locais pré-existentes no sistema (ex: `~/.config/bspwm`), o script **cria automaticamente um backup prévio** em:
`~/.dotfiles_backup/YYYYMMDD_HHMMSS/`
evitando qualquer perda acidental de dados.
