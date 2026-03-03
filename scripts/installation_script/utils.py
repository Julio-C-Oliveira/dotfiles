import logging

import argparse
import json

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

    for category, pkgs in packages_dict.items():
        logger.info(f"Instalando categoria: {category_name}")
        
        run(
            command=f"sudo pacman -S --needed --noconfirm {' '.join(pkgs)}", 
            logger=logger
        )

def install_yay_packages(packages, logger):
    logger.info("Instalando pacotes do AUR pelo yay")

    for category, pkgs in packages_dict.items():
        logger.info(f"Instalando categoria: {category_name}")
        
        run(
            command=f"yay -S --needed --noconfirm {' '.join(pkgs)}", 
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
        pkg = pkg_data["name"]
        targets = pkg_data["target"]
        
        for target in targets:
            target_path = home / target
            
            if target_path.exists() or target_path.is_symlink():
                logger.debug(f"Limpando conflito em: {target_path}")
                
                try:
                    if target_path.is_dir() and not target_path.is_symlink():
                        shutil.rmtree(target_path)
                    else:
                        target_path.unlink()
                except Exception as e:
                    logger.error(f"Erro ao remover {target_path}: {e}")

        run(
            command=f"stow {pkg}",
            logger=logger
        )

    os.chdir(home)

def apply_sddm_stow(stow_path, logger):
    logger.info("Configurando o sddm")

    home = Path.home()
    path = (home / stow_path).resolve()
    os.chdir(path)

    run(
        command="sudo stow -t / sddm",
        logger=logger
    )
    run(
        command="sudo cp wallpapers/Moon_Rukia.jpg /usr/share/sddm/themes/sugar-candy/Backgrounds/Mountain.jpg",
        logger=logger
    )

    os.chdir(home)

def setup_packages(packages, logger):
    logger.info("Inciando a configuração dos pacotes")

    home = Path.home()
    os.chdir(home)

    for pkg_data in packages:
        pkg_name = pkg_data["package"]
        commands = pkg_data["commands"]

        logger.info(f"Configurando o pacote: {pkg_name}")

        for command in commands:
            run(
                command=command,
                logger=logger   
            )

    os.chdir(home)

def update_grub(logger):
    if Path("/boot/grub/grub.cfg").exists():
        logger.info("Gerando nova configuração do GRUB para carregar o ucode")
        run(
            command="sudo grub-mkconfig -o /boot/grub/grub.cfg", 
            logger=logger
        )
    else:
        logger.warning("GRUB não encontrado em /boot. Atualize manualmente.")

def unpack_wallpapers(zip_path, zip_name, output_path, logger):
    logger.info("Descomprimindo o zip com os wallpapers.")

    home = Path.home()
    path = (home / zip_path).resolve()
    file_path = (path / zip_name).resolve()
    os.chdir(path)

    run(
        command=f"7z x {file_path} -o{output_path}",
        logger=logger
    )

    os.chdir(home)

def unpack_sddm_theme(zip_path, zip_name, logger):
    logger.info("Descomprimindo o zip com o tema do sddm.")

    home = Path.home()
    path = (home / zip_path).resolve()
    file_path = (path / zip_name).resolve()
    os.chdir(path)

    run(
        command=f"7z x {file_path}",
        logger=logger
    )

    run(
        command="sudo mv sugar-candy /usr/share/sddm/themes/",
        logger=logger
    )

    run(
        command=f"sudo cp wallpapers/Moon_Rukia.jpg /usr/share/sddm/themes/sugar-candy/Backgrounds/Mountain.jpg",
        logger=logger
    )

    os.chdir(home)


def install_video_drivers(logger):
    logger.info("Instalando os drivers de video")

    run(
        command="sudo pacman -S --needed --noconfirm mesa libva-mesa-driver mesa-utils",
        logger=logger
    )
    try:
        output = subprocess.check_output("lspci | grep -E 'VGA|3D'", shell=True).decode().lower()
        video_driver = ""
        vulkan_driver = ""

        match output:
            case _ if "nvidia" in output:
                video_driver = "nvidia"
            case _ if "amd" in output or "ati" in output:
                video_driver = "xf86-video-amdgpu"
                vulkan_driver = "vulkan-radeon"
            case _ if "intel" in output:
                video_driver = "mesa" 
                vulkan_driver = "vulkan-intel"
            case _ if "virtualbox" in output or "vmware" in output:
                video_driver = "virtualbox-guest-utils"
            case _:
                video_driver = "xf86-video-vesa"
    except:
        video_driver = "xf86-video-vesa"

    run(
        command=f"sudo pacman -S --needed --noconfirm {video_driver} {vulkan_driver}",
        logger=logger
    )

def setup_gui(logger):
    choice = input("[1] - startx\n[2] - sddm\nchoice: ")

    logger.info(f"Configurando a GUI, sua escolha: {"startx" if choice == "1" else "sddm"}")

    install_video_drivers(logger)

    if choice == "2": setup_sddm(
        zip_path="dotfiles",
        zip_name="sddm_theme.7z",
        stow_path="dotfiles",
        logger=logger
    )
    else: setup_startx(
        packages=[("xorg", ".xinitrc")],
        stow_path="dotfiles",
        logger=logger
    )

def setup_sddm(zip_path, zip_name, stow_path, logger):
    run(
        command="sudo pacman -S --needed --noconfirm sddm qt5-graphicaleffects qt5-quickcontrols2 qt5-svg",
        logger=logger
    )

    run(
        command="sudo systemctl enable sddm",
        logger=logger
    )

    unpack_sddm_theme(
        zip_path=zip_path,
        zip_name=zip_name,
        logger=logger
    )

    apply_sddm_stow(
        stow_path=stow_path, 
        logger=logger
    )

def setup_startx(packages, stow_path, logger):
    run(
        command="sudo pacman -S --needed --noconfirm xorg-xinit",
        logger=logger
    )

    apply_stow(
        packages=packages,
        stow_path=stow_path,
        logger=logger
    )

def get_parse_args(logger):
    parser = argparse.ArgumentParser(description="Script de pós instalação do Arch")
    
    parser.add_argument(
        "-c", "--config", 
        default="packages.json", 
        help="Caminho pro JSON com as configurações (Padrão: packages.json)"
    )
    
    args = parser.parse_args()

    logger.info(f"Caminho do json: {args.config}")
    return args

def load_json(parse_args, logger):
    try:
        with open(parse_args.config, 'r') as f:
            config = json.load(f)
        logger.info(f"{parse_args.config} carregado com sucesso")
        return config
    except FileNotFoundError:
        logger.error(f"Arquivo '{parse_args.config}' não encontrado.")
        sys.exit(1)
        return
    except json.JSONDecodeError:
        logger.error(f"O arquivo '{parse_args.config}' não é um JSON válido.")
        sys.exit(1)
        return