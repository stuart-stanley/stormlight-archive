#!/usr/bin/env bash

export APP_PACKAGE_LOCATION=/usr/local/stormlight_archive/stormlight_archive
export DEV_USER=stuarts

if [[ ${STORMLIGHT_ARCHIVE__START_SSH} -eq 1 ]] ; then
    service ssh start
fi


# Do the other half of setup_dev_user.sh and populate the /home/${DEV_USER}
# persistent volume. Note we do this before turning on 'set -x' because really,
# this isn't mission critical.
su ${DEV_USER} --login --pty --shell /bin/bash ${APP_PACKAGE_LOCATION}/ci/templates/dev_user/setup_dev_user_container_start.sh


if [ ${BALENA} ] ; then
    # give us a nicer hostname when logging in!
    hostname -b ${BALENA_DEVICE_NAME_AT_INIT}

    # add our hostname to /etc/hosts so we can use ssh-x11-forward
    echo "127.0.1.1 ${BALENA_DEVICE_NAME_AT_INIT}" >> /etc/hosts

    printenv > ~/startup_based_env_var.env

    ${APP_PACKAGE_LOCATION}/bin/container_x11_target.sh
elif [ ${INSIDE_DOCKER_COMPOSE} ] ; then
    printenv > ~/startup_based_env_var.env
    ${APP_PACKAGE_LOCATION}/bin/container_x11_target.sh
else
    echo "NOT running in Balena, so just going to sleep to allow devmod"
    sleep 999999
fi
