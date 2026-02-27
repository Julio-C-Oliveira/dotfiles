import logging

import sys
from pathlib import Path

import os
import shutil

import subprocess

class Cores:
    RESET = "\033[0m"
    BOLD_PURPLE = "\033[1;35m"
    CYAN = "\033[36m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    RED = "\033[31m"
    BOLD_RED = "\033[1;31m"

class CustomColorFormatter(logging.Formatter):
    LEVEL_COLORS = {
        logging.DEBUG: Cores.CYAN,
        logging.INFO: Cores.GREEN,
        logging.WARNING: Cores.YELLOW,
        logging.ERROR: Cores.RED,
        logging.CRITICAL: Cores.BOLD_RED,
    }

    def format(self, record):
        level_color = self.LEVEL_COLORS.get(record.levelno, Cores.RESET)
        asctime_color = Cores.BOLD_PURPLE
        
        format_str = (
            f"{asctime_color}%(asctime)s{Cores.RESET} "
            f"[{level_color}%(levelname)s{Cores.RESET}] "
            f"[%(name)s] %(message)s"
        )
        
        formatter = logging.Formatter(format_str, datefmt="%Y-%m-%d %H:%M:%S")
        return formatter.format(record)

def setup_logger(name, log_file, logs_folder, level=logging.DEBUG):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    if logger.hasHandlers():
        logger.handlers.clear()

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(CustomColorFormatter())

    logs_path = Path(logs_folder)
    logs_path.mkdir(parents=True, exist_ok=True)
    log_file_path = logs_path / log_file
    
    file_handler = logging.FileHandler(log_file_path)
    file_formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(file_formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger

def run(command, logger, shell=False):
    try:
        cmd = command if shell else command.split()
        subprocess.run(cmd, check=True)
        logger.debug(f"Sucesso ao executar: {command}")
    except subprocess.CalledProcessError as e:
        logger.error(f"Erro ao executar: {command}")
        exit(1)

def install_arch_packages(packages, logger):
    logger.info("Instalando pacotes do Arch")

    run(
        command=f"sudo pacman -S --needed --noconfirm {' '.join(packages)}", 
        logger=logger
    )

def install_yay_packages(packages, logger):
    logger.info("Instalando pacotes do AUR pelo yay")
    
    run(
        command=f"yay -S --needed --noconfirm {' '.join(packages)}",
        logger=logger
    )

def install_ucode(logger):
    logger.info("Verificando qual ucode instalar")
    try:
        with open("/proc/cpuinfo", "r") as f:
            cpuinfo = f.read().lower()
            if "intel" in cpuinfo:
                run(
                    command="sudo pacman -S --needed --noconfirm intel-ucode",
                    logger=logger
                )
            elif "amd" in cpuinfo:
                run(
                    command="sudo pacman -S --needed --noconfirm amd-ucode",
                    logger=logger
                    )
                
    except Exception as e:
        logger.error(f"Erro ao ler cpuinfo: {e}")

def install_yay(logger):
    logger.info("Verificando se o yay já está instalado")

    if shutil.which("yay"):
        logger.debug("Yay já instalado")
        return

    logger.info("Instalando as dependências do yay")
    run(
        command="sudo pacman -S --needed --noconfirm git base-devel",
        logger=logger
    )

    logger.info("Instalando o yay")

    run(
        command="git clone https://aur.archlinux.org/yay.git /tmp/yay",
        logger=logger
    )
    os.chdir("/tmp/yay")
    run(
        command="makepkg -si --noconfirm",
        logger=logger
    )
    os.chdir(os.path.expanduser("~"))

def enable_system_services(packages, logger):
    logger.info("Habilitando os serviços")

    run(
        command=f"sudo systemctl enable {' '.join(packages)}",
        logger=logger
    )

def enable_user_services(packages, logger):
    logger.info("Habilitando os serviços do usuário")

    run(
        command=f"systemctl --user enable {' '.join(packages)}",
        logger=logger
    )

def apply_stow(packages, stow_path, logger):
    logger.info("Iniciando a aplicação do stow")

    home = Path.home()
    path = (home / stow_path).resolve()
    os.chdir(path)
    
    for pkg_data in packages:
        pkg, *targets = pkg_data
        
        for target in targets:
            target_path = home / target
            
            if target_path.exists() or target_path.is_symlink():
                logger.debug(f"Limpando: {target_path}")
                
                if target_path.is_dir() and not target_path.is_symlink():
                    shutil.rmtree(target_path)
                else:
                    target_path.unlink()
        
        run(
            command=f"stow {pkg}",
            logger=logger
        )

def setup_ufw(logger):
    logger.info("Configurando regras básicas do ufw")
    run(
        command="sudo ufw default deny incoming", 
        logger=logger
    )
    run(
        command="sudo ufw default allow outgoing", 
        logger=logger
    )
    run(
        command="sudo ufw enable", 
        logger=logger
    )

def update_grub(logger):
    if Path("/boot/grub/grub.cfg").exists():
        logger.info("Gerando nova configuração do GRUB para carregar o ucode")
        run(
            command="sudo grub-mkconfig -o /boot/grub/grub.cfg", 
            logger=logger
        )
    else:
        logger.warning("GRUB não encontrado em /boot. Atualize manualmente.")