# Repositório de Dotfiles & Gestão de Sistemas

Repositório para armazenar meus dotfiles, configurações do sistema Linux e scripts de automação/instalação.

---

## 🛠️ Fluxo do Agente Spec Kit (Dotfiles)

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

### 📋 Estágios do Fluxo

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

## 🔍 Novos Comandos Específicos para Dotfiles

Além do fluxo principal de especificação e desenvolvimento, o repositório conta com comandos utilitários dedicados à auditoria e sincronização do sistema Linux:

| Comando | Descrição & Uso |
| :--- | :--- |
| **`/speckit-audit-install`** | **Auditoria do Script de Instalação**: Analisa se o script de instalação (`scripts/installation_script/`) e a lista de pacotes (`packages.json`) estão 100% coerentes e sincronizados com as pastas de dotfiles existentes no repositório. |
| **`/speckit-detect-drift`** | **Detecção de Mudanças Externas**: Compara o ambiente ativo do sistema (`~/.config`, `/etc`, etc.) com os arquivos versionados no repositório, identificando alterações locais não commitadas ou novos aplicativos elegíveis para importação. |
| **`/speckit-ignore`** | **Gerenciamento do `.dotfilesignore`**: Visualiza, testa ou adiciona regras ao arquivo `.dotfilesignore` (ou `.agentignore`), definindo quais arquivos, caches, logs ou segredos o agente deve ignorar durante as varreduras. |

---

## 🛡️ Arquivo de Exclusões (`.dotfilesignore`)

O arquivo [.dotfilesignore](file:///home/julio/dotfiles/.dotfilesignore) serve pro agente ignorar:
- **Segredos e Credenciais**: Chaves SSH (`id_rsa`), certificados (`*.pem`, `*.key`), tokens de nuvem/API.
- **Logs e Caches**: `install.log`, `__pycache__/`, `*.pyc`, diretórios `.cache/`.
- **Dumps Binários**: Compactados grandes (`.7z`, `.iso`, `.tar.gz`) que não devem ir ao Git sem LFS.
- **Estado Temporário**: `.swp`, `Thumbs.db`, `.DS_Store`.
