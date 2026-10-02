import json
import utils
import argparse
import sys

def main():
    logger = utils.setup_logger(
        name="Arch",
        log_file="install.log",
        logs_folder="./"
    )

    parse_args = utils.get_parse_args(
        logger=logger
    )

    repo_root = utils.get_repo_root(
        custom_path=parse_args.repo_dir
    )
    logger.info(f"Raiz do repositório detectada: {repo_root}")

    configs = utils.load_json(
        parse_args=parse_args,
        repo_root=repo_root,
        logger=logger
    )

    utils.setup_pacman(
        logger=logger
    )

    logger.info("Atualizando o sistema")
    utils.run(
        command="sudo pacman -Syu --noconfirm",
        logger=logger
    )

    utils.install_arch_packages(
        packages=configs["arch_packages"],
        logger=logger
    )

    utils.install_yay(
        logger=logger
    )

    utils.install_yay_packages(
        packages=configs["yay_packages"],
        logger=logger
    )

    utils.install_ucode(
        logger=logger
    )

    utils.enable_system_services(
        packages=configs["system_packages_to_enable"],
        logger=logger
    )

    utils.enable_user_services(
        packages=configs["user_packages_to_enable"],
        logger=logger
    )

    utils.unpack_wallpapers(
        repo_root=repo_root,
        zip_name="wallpapers.7z",
        output_path="./wallpapers",
        logger=logger
    )

    utils.setup_directories(
        logger=logger
    )

    utils.apply_stow(
        packages=configs["stow_packages"],
        repo_root=repo_root,
        logger=logger
    )

    utils.setup_gui(
        logger=logger,
        gui_choice=parse_args.gui,
        non_interactive=parse_args.non_interactive,
        repo_root=repo_root
    )

    utils.setup_packages(
        packages=configs["packages_to_setup"],
        repo_root=repo_root,
        logger=logger
    )

    utils.run(
        command="dbus-launch gsettings set org.gnome.desktop.interface color-scheme 'prefer-dark'",
        logger=logger,
        shell=True
    )

    utils.setup_plymouth(
        repo_root=repo_root,
        logger=logger
    )

    utils.update_grub(
        logger=logger
    )

    logger.info("Instalação finalizada com sucesso!")
    
    do_reboot = False
    if parse_args.reboot:
        do_reboot = True
    elif parse_args.no_reboot or parse_args.non_interactive:
        do_reboot = False
    else:
        confirmar = input(f"\n{utils.Cores.YELLOW}Deseja reiniciar o sistema agora? (s/n): {utils.Cores.RESET}")
        if confirmar.strip().lower() == 's':
            do_reboot = True

    if do_reboot:
        logger.info("Reiniciando o sistema...")
        utils.run(
            command="sudo reboot", 
            logger=logger
        )

if __name__ == "__main__":
    main()