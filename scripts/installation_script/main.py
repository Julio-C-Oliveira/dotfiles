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

    configs = utils.load_json(
        parse_args=parse_args,
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
        zip_path="dotfiles",
        zip_name="wallpapers.7z",
        output_path="./wallpapers",
        logger=logger
    )

    utils.apply_stow(
        packages=configs["stow_packages"],
        stow_path="dotfiles",
        logger=logger
    )

    utils.setup_gui(
        logger=logger
    )

    utils.setup_packages(
        packages=configs["packages_to_setup"],
        logger=logger
    )

    utils.update_grub(
        logger=logger
    )

    logger.info("Instalação finalizada")
    
    confirmar = input(f"\n{utils.Cores.YELLOW}Deseja reiniciar o sistema agora? (s/n): {utils.Cores.RESET}")
    if confirmar.lower() == 's':
        utils.run(
            command="sudo reboot", 
            logger=logger
        )

    
if __name__ == "__main__":
    main()