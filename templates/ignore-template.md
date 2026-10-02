# Dotfiles & Agent Ignore Rules (.dotfilesignore / .agentignore)
# Standard ignore patterns for dotfiles repositories and agent file scanners

# Secrets and Sensitive Credentials (NON-NEGOTIABLE)
*.pem
*.key
*.p12
*.pfx
*.asc
id_rsa
id_rsa.pub
id_ed25519
id_ed25519.pub
.ssh/
.gnupg/
.aws/
.kube/
.vault-token
*.secret
*.env

# Installation Logs & Caches
*.log
install.log
__pycache__/
*.pyc
*.pyo
.cache/
.npm/
.cargo/bin/
.cargo/registry/

# Compressed Archives & Large Binary Dumps
*.7z
*.tar.gz
*.zip
*.iso

# Local OS & Editor Temporary State
.DS_Store
Thumbs.db
*.swp
*.swo
*~
.idea/
.vscode/

# Application Caches / Socket Files / Dynamic Runtime State
*.sock
*.pid
