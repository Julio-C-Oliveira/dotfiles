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
        subprocess.run(cmd, check=True, shell=shell)
        logger.debug(f"Sucesso ao executar: {command}")
    except subprocess.CalledProcessError as e:
        logger.error(f"Erro ao executar: {command}")
        exit(1)

def setup_pacman(logger):
    logger.info("Configurando o pacman.conf")
    
    pacman_conf = "/etc/pacman.conf"

    commands = [
        f"sudo sed -i 's/^#Color/Color/' {pacman_conf}",
        f"grep -q 'ILoveCandy' {pacman_conf} || sudo sed -i '/^Color/a ILoveCandy' {pacman_conf}",
        f"sudo sed -i 's/^#CheckSpace/CheckSpace/' {pacman_conf}",
        f"sudo sed -i 's/^#ParallelDownloads/ParallelDownloads/' {pacman_conf}",
        f"sudo sed -i '/^#\[multilib\]/,/^#Include = \/etc\/pacman.d\/mirrorlist/ s/^#//' {pacman_conf}"
    ]

    for command in commands:
        run(
            command=command,
            logger=logger,
            shell=True
        )

def install_arch_packages(packages, logger):
    logger.info("Instalando pacotes do Arch")

    for category, pkgs in packages.items():
        logger.info(f"Instalando categoria: {category}")
        
        run(
            command=f"sudo pacman -S --needed --noconfirm {' '.join(pkgs)}", 
            logger=logger
        )

def install_yay_packages(packages, logger):
    logger.info("Instalando pacotes do AUR pelo yay")

    for category, pkgs in packages.items():
        logger.info(f"Instalando categoria: {category}")
        
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

def get_repo_root(custom_path=None):
    if custom_path:
        return Path(custom_path).resolve()
    # utils.py is located at scripts/installation_script/utils.py
    return Path(__file__).resolve().parent.parent.parent

def backup_conflict(target_path, backup_dir, logger):
    if target_path.is_symlink():
        logger.debug(f"Removendo link simbólico existente: {target_path}")
        target_path.unlink()
    elif target_path.exists():
        home = Path.home()
        try:
            rel_target = target_path.relative_to(home)
        except ValueError:
            rel_target = target_path.name
        
        dest = backup_dir / rel_target
        dest.parent.mkdir(parents=True, exist_ok=True)
        logger.info(f"Criando backup de conflito: {target_path} -> {dest}")
        shutil.move(str(target_path), str(dest))

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

    if os.path.exists("/tmp/yay"):
        shutil.rmtree("/tmp/yay")

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

def apply_stow(packages, repo_root, logger):
    logger.info("Iniciando a aplicação do stow")

    home = Path.home()
    repo_path = Path(repo_root).resolve()
    os.chdir(repo_path)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = home / ".dotfiles_backup" / timestamp

    for pkg_data in packages:
        pkg = pkg_data["name"]
        targets = pkg_data["target"]
        
        for target in targets:
            target_path = home / target
            
            if target_path.exists() or target_path.is_symlink():
                logger.debug(f"Tratando conflito em: {target_path}")
                try:
                    backup_conflict(target_path, backup_dir, logger)
                except Exception as e:
                    logger.error(f"Erro ao tratar conflito em {target_path}: {e}")

        run(
            command=f"stow {pkg}",
            logger=logger
        )

    os.chdir(home)

def apply_sddm_stow(repo_root, logger):
    logger.info("Configurando o sddm via Stow")

    home = Path.home()
    repo_path = Path(repo_root).resolve()
    os.chdir(repo_path)

    run(
        command="sudo stow -t / sddm",
        logger=logger
    )

    wallpaper_path = repo_path / "wallpapers" / "Moon_Rukia.jpg"
    run(
        command=f"sudo cp {wallpaper_path} /usr/share/sddm/themes/sugar-candy/Backgrounds/Mountain.jpg",
        logger=logger
    )

    os.chdir(home)

def setup_packages(packages, repo_root, logger):
    logger.info("Iniciando a configuração dos pacotes")

    home = Path.home()
    os.chdir(home)
    repo_path = Path(repo_root).resolve()

    for pkg_data in packages:
        pkg_name = pkg_data["package"]
        commands = pkg_data["commands"]

        logger.info(f"Configurando o pacote: {pkg_name}")

        for command in commands:
            cmd = command.replace("~/dotfiles", str(repo_path))
            run(
                command=cmd,
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

def unpack_wallpapers(repo_root, zip_name, output_path, logger):
    logger.info("Descomprimindo o zip com os wallpapers.")

    home = Path.home()
    repo_path = Path(repo_root).resolve()
    file_path = repo_path / zip_name
    os.chdir(repo_path)

    out_full = (repo_path / output_path).resolve()
    run(
        command=f"7z x {file_path} -o{out_full} -y",
        logger=logger
    )

    os.chdir(home)

def unpack_sddm_theme(repo_root, zip_name, logger):
    logger.info("Descomprimindo o zip com o tema do sddm.")

    home = Path.home()
    repo_path = Path(repo_root).resolve()
    file_path = repo_path / zip_name
    os.chdir(repo_path)

    run(
        command=f"7z x {file_path} -y",
        logger=logger
    )

    run(
        command="sudo rm -rf /usr/share/sddm/themes/sugar-candy && sudo mv sugar-candy /usr/share/sddm/themes/",
        logger=logger,
        shell=True
    )

    wallpaper_path = repo_path / "wallpapers" / "Moon_Rukia.jpg"
    run(
        command=f"sudo cp {wallpaper_path} /usr/share/sddm/themes/sugar-candy/Backgrounds/Mountain.jpg",
        logger=logger
    )

    os.chdir(home)


def setup_plymouth(repo_root, logger):
    logger.info("Configurando o tema Plymouth umamusume...")

    repo_path = Path(repo_root).resolve()
    plymouth_src = repo_path / "plymouth" / "umamusume"
    plymouth_target = Path("/usr/share/plymouth/themes/umamusume")

    if plymouth_src.exists():
        run(
            command=f"sudo mkdir -p {plymouth_target}",
            logger=logger
        )
        run(
            command=f"sudo cp -r {plymouth_src}/* {plymouth_target}/",
            logger=logger,
            shell=True
        )
        run(
            command="sudo plymouth-set-default-theme -R umamusume",
            logger=logger
        )
    else:
        logger.warning(f"Diretório {plymouth_src} não encontrado.")


def install_video_drivers(logger):
    logger.info("Instalando os drivers de vídeo")

    run(
        command="sudo pacman -S --needed --noconfirm mesa lib32-mesa libva-mesa-driver mesa-utils",
        logger=logger
    )
    try:
        output = subprocess.check_output("lspci | grep -E 'VGA|3D'", shell=True).decode().lower()

        match output:
            case _ if "nvidia" in output:
                packages = ["nvidia", "nvidia-utils", "lib32-nvidia-utils"]
            case _ if "amd" in output or "ati" in output:
                packages = ["xf86-video-amdgpu", "vulkan-radeon", "lib32-vulkan-radeon"]
            case _ if "intel" in output:
                packages = ["mesa", "vulkan-intel", "lib32-vulkan-intel"]
            case _ if "virtualbox" in output or "vmware" in output:
                packages = ["virtualbox-guest-utils"]
            case _:
                packages = ["xf86-video-vesa"]
    except:
        packages = ["xf86-video-vesa"]

    run(
        command=f"sudo pacman -S --needed --noconfirm {' '.join(packages)}",
        logger=logger
    )

def setup_gui(logger, gui_choice=None, non_interactive=False, repo_root=None):
    choice = None
    if gui_choice:
        choice = gui_choice.lower()
    elif non_interactive:
        logger.info("Modo não-interativo ativado. Escolhendo opção padrão de GUI: sddm")
        choice = "sddm"
    else:
        user_in = input("[1] - startx\n[2] - sddm\nchoice: ").strip()
        choice = "startx" if user_in == "1" else "sddm"

    gui_name = "startx" if choice in ["1", "startx"] else "sddm"
    logger.info(f"Configurando a GUI, sua escolha: {gui_name}")

    install_video_drivers(logger)

    if gui_name == "sddm":
        setup_sddm(
            zip_name="sddm_theme.7z",
            repo_root=repo_root,
            logger=logger
        )
    else:
        setup_startx(
            packages=[{"name": "xorg", "target": [".xinitrc"]}],
            repo_root=repo_root,
            logger=logger
        )

def setup_sddm(zip_name, repo_root, logger):
    run(
        command="sudo pacman -S --needed --noconfirm sddm qt5-graphicaleffects qt5-quickcontrols2 qt5-svg",
        logger=logger
    )

    run(
        command="sudo systemctl enable sddm",
        logger=logger
    )

    unpack_sddm_theme(
        zip_name=zip_name,
        repo_root=repo_root,
        logger=logger
    )

    apply_sddm_stow(
        repo_root=repo_root, 
        logger=logger
    )

def setup_startx(packages, repo_root, logger):
    run(
        command="sudo pacman -S --needed --noconfirm xorg-xinit",
        logger=logger
    )

    apply_stow(
        packages=packages,
        repo_root=repo_root,
        logger=logger
    )

def setup_directories(logger):
    logger.info("Criando os diretórios.")

    run(
        command="mkdir -p ~/.config ~/{downloads,templates,public,music,videos} ~/pictures/screenshots ~/documents/github ~/desktop/{current_work,temporary}",
        logger=logger
    )

def get_parse_args(logger):
    parser = argparse.ArgumentParser(description="Script de pós-instalação do Arch Linux")
    
    parser.add_argument(
        "-c", "--config", 
        default="packages.json", 
        help="Caminho pro JSON com as configurações (Padrão: packages.json)"
    )

    parser.add_argument(
        "-g", "--gui",
        choices=["sddm", "startx"],
        default=None,
        help="Escolha da interface gráfica (sddm ou startx)"
    )

    parser.add_argument(
        "-y", "--yes", "--non-interactive",
        dest="non_interactive",
        action="store_true",
        help="Executar instalação sem confirmações / modo não-interativo"
    )

    parser.add_argument(
        "--reboot",
        action="store_true",
        default=False,
        help="Reiniciar o sistema automaticamente ao final"
    )

    parser.add_argument(
        "--no-reboot",
        action="store_true",
        default=False,
        help="Não reiniciar o sistema ao final"
    )

    parser.add_argument(
        "--repo-dir",
        default=None,
        help="Caminho raiz do repositório dotfiles (Padrão: detectado automaticamente)"
    )
    
    args = parser.parse_args()

    logger.info(f"Caminho do json: {args.config}")
    return args

def load_json(parse_args, repo_root, logger):
    config_path = Path(parse_args.config)
    if not config_path.is_absolute():
        if not config_path.exists():
            candidate = repo_root / "scripts" / "installation_script" / config_path
            if candidate.exists():
                config_path = candidate

    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        logger.info(f"{config_path} carregado com sucesso")
        return config
    except FileNotFoundError:
        logger.error(f"Arquivo '{config_path}' não encontrado.")
        sys.exit(1)
    except json.JSONDecodeError:
        logger.error(f"O arquivo '{config_path}' não é um JSON válido.")
        sys.exit(1)