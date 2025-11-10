#!/usr/bin/env bash
#
# This one is run from container_startup.sh to see if in-directory setup still needs to
# occur for the dev-user.
#
# It must be run as "su ${DEV_USER_NAME} --login --command path/setup_dev_user_container_start.sh"
#
# TODO: pass APP_PACKAGE_LOCATION in instead of redefining here
# TODO: ditto for DEV_USER_NAME
export DEV_USER_NAME=stuarts
APP_PACKAGE_LOCATION=/usr/local/stormlight_archive/stormlight_archive

set -x
if [ ! -d /home/${DEV_USER_NAME} ] ; then
    mkdir -p /home/${DEV_USER_NAME}
    mkdir -p /home/${DEV_USER_NAME}/.ssh
    rsync -av /etc/skel/ /home/${DEV_USER_NAME}
    chown -R ${DEV_USER_NAME}:${DEV_USER_NAME} /home/${DEV_USER_NAME}
fi
if [ ! -d /home/${DEV_USER_NAME}/.oh-my-zsh/ ] ; then
    curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh > install.sh
    chmod +x install.sh
    sh ./install.sh --unattended
    rm install.sh
    # overwrite the default here
    cp ${APP_PACKAGE_LOCATION}/ci/templates/${DEV_USER_NAME}_user/dot_zshrc.template /home/${DEV_USER_NAME}/.zshrc
fi
if [ ! -d /home/${DEV_USER_NAME}/.oh-my-zsh/custom/themes/Ducula ] ; then
    ZSH_CUSTOM=/home/nfgsw/.oh-my-zsh/custom
    git clone https://github.com/janjoswig/Ducula.git ${ZSH_CUSTOM}/themes/Ducula
fi
if [ ! -f /home/${DEV_USER_NAME}/.zshrc ] ; then
    cp ${APP_PACKAGE_LOCATION}/ci/templates/dot_zshrc.template /home/${DEV_USER_NAME}/.zshrc
fi
if [ ! -f /home/${DEV_USER_NAME}/.emacs ] ; then
     cp ${APP_PACKAGE_LOCATION}/ci/templates/dot_emacs.template /home/${DEV_USER_NAME}/.emacs
fi
if [ ! -d /home/${DEV_USER_NAME}/.iterm2 ] ; then
    curl -L https://iterm2.com/shell_integration/install_shell_integration_and_utilities.sh | zsh
fi
if [ ! -f /home/${DEV_USER_NAME}/.iterm2_shell_integration.zsh ] ; then
    curl -L https://iterm2.com/shell_integration/zsh -o ~/.iterm2_shell_integration.zsh
    chmod +x  ~/.iterm2_shell_integration.zsh
fi
