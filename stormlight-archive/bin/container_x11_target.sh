#!/usr/bin/env bash

export DISPLAY=:0
export DBUS_SYSTEM_BUS_ADDRESS=unix:path=/host/run/dbus/system_bus_socket

echo "waiting for X11"
while ! xset -q; do sleep 0.5; done
echo "X11 is up"


xset s off       # don't activate screen saver
xset -dpms       # disable DPMS (Energy Star) features.
xset s noblank   # don't blank the video device.
# TODO: remove? unclutter&       # hide the mouse pointer if its not moving:


cd ${APP_PACKAGE_LOCATION}

while ( true ) ; do
    if [[ ${LINE_LABEL_SYSTEM_FIXTURE_START_MODE} = "app" ]] ; then
        echo "we will get to this...."
        bin/try_app_start.sh
    elif [[ ${LINE_LABEL_SYSTEM_FIXTURE_START_MODE} = "xterm" ]]; then
        uxterm -fullscreen
    else
        echo "WARNING: Unset LINE_LABEL_SYSTEM_FIXTURE_START_MODE env variable. Permitted values: app, xterm"
    fi
    echo "core-app exited. Restarting it in 5 seconds"
    sleep 5
done
