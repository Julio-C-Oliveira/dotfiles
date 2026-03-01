import utils, packages

logger = utils.setup_logger(
    name="Arch",
    log_file="install.log",
    logs_folder="./"
)

def main():
    logger.info("Atualizando o sistema")
    utils.run(
        command="sudo pacman -Syu --noconfirm",
        logger=logger
    )

    utils.install_arch_packages(
        packages=packages.arch_packages,
        logger=logger
    )

    utils.install_yay(
        logger=logger
    )

    utils.install_yay_packages(
        packages=packages.yay_packages,
        logger=logger
    )

    utils.install_ucode(
        logger=logger
    )

    utils.enable_system_services(
        packages=packages.system_packages_to_enable,
        logger=logger
    )

    utils.enable_user_services(
        packages=packages.user_packages_to_enable,
        logger=logger
    )

    utils.unpack_wallpapers(
        zip_path="dotfiles",
        zip_name="wallpapers.7z",
        output_path="./wallpapers",
        logger=logger
    )

    utils.apply_stow(
        packages=packages.stow_packages,
        stow_path="dotfiles",
        logger=logger
    )

    utils.unpack_sddm_theme(
        zip_path="dotfiles",
        zip_name="sddm_theme.7z",
        logger=logger
    )

    utils.apply_sddm_stow(
        stow_path="dotfiles", 
        logger=logger
    )

    utils.setup_packages(
        packages=packages.packages_to_setup,
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