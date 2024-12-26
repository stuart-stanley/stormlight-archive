#!/usr/bin/env bash

#
# really rough setup of mfgsw user. We want this to live in a persistant space between balena deploys
# thus allows "local" work to be done. It gets tricky because each time we build,
# the /etc space is brand new.
#
# So this become a two part thing:
#  1) here, we make the user to populate /etc. We let it make the /home/mfgsw directory, but...
#  2) that will vanish (be overlayed by the persistant volume), so we put off filling it in
#     until bin/container_start.sh


useradd --shell /bin/zsh --groups dialout,video --create-home --home-dir /home/mfgsw mfgsw

# make a big random password for mfgsw to allow sshd to use it.
# also make it so sshd WON'T use it.
usermod mfgsw --password $(openssl rand -base64 32)
usermod mfgsw --unlock

echo "PasswordAuthentication no" >> /etc/ssh/sshd_config
# allow X11 forwarding to actually work.
echo "AddressFamily inet" >> /etc/ssh/sshd_config
# and turn it on
echo "X11Forwarding yes" >> /etc/ssh/sshd_config
