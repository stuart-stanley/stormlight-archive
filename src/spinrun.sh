#!/usr/bin/env bash
cd /home/pi/stormlight-archive/src

while(true) ; do
    sudo python main.py
    ecode=$?
    if [ ${ecode} != 0 ]; then
	date
	sudo tar -czf failsnap.tgz -C/var ./log
	exit 99
    fi
    #sleep 10
done
