#!/usr/bin/env bash

while(true) ; do
    # sudo python main.py
    python main.py
    ecode=$?
    if [ ${ecode} != 0 ]; then
	date
	tar -czf failsnap.tgz -C/var ./log
	exit 99
    fi
    #sleep 10
done
