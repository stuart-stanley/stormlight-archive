#!/usr/bin/env bash

export APP_PACKAGE_LOCATION=/usr/local/line_label_system/line_label_system_gf_ms

if [[ ${LINE_LABEL_SYSTEM_START_SSH} -eq 1 ]] ; then
    service ssh start
fi


# Do the other half of setup_mfgsw_user.sh and populate the /home/mfgsw
# persistent volume. Note we do this before turning on 'set -x' because really,
# this isn't mission critical.
su mfgsw --login --pty --shell /bin/bash ${APP_PACKAGE_LOCATION}/ci/templates/mfgsw_user/setup_mfgsw_user_container_start.sh

# Make /dev/console writeable by non-priv. Nicer would be ACLs, but that requires systemd et al.
chmod 0622 /dev/console


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
