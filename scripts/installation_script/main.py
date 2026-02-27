import utils, packages

logger = utils.setup_logger(
    name="Arch",
    log_file="install.log",
    logs_folder="./"
)

def main():
    logger.info("Atualizando o sistema")
    utils.run("sudo pacman -Syu --noconfirm")

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
        system_packages_to_enable=packages.system_packages_to_enable,
        logger=logger
    )

    utils.apply_stow(
        packages=packages.stow_packages,
        stow_path="dotfiles",
        logger=logger
    )

    utils.setup_ufw(
        logger=logger
    )

    utils.update_grub(
        logger=logger
    )

if __name__ == "__main__":
    main()