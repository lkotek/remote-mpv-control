#!/bin/bash

IPC_SOCKET=/tmp/remote-mpv-control-socket
CONFIG_PATH=~/.remote-mpv-control
PLAYLIST_POSITION_PATH=/tmp/remote-mpv-playlist-pos

if [ -d $CONFIG_PATH ]; then
    echo
    echo "Configuration already exists! If you want to create new one, run:"
    echo
    echo "rm -rf $CONFIG_PATH"
    echo
    exit 1
fi

read -p "Set IPv4 address for web UI: " WEB_IP
read -p "Set port for web UI: " WEB_PORT
read -p "Set step for volume: " VOLUME_STEP

mkdir $CONFIG_PATH

echo "[GENERAL]

install_path=${PWD}
ipc_socket=${IPC_SOCKET}
playlist_position_path=${PLAYLIST_POSITION_PATH}
volume_step=${VOLUME_STEP}

[WEB]

ip=${WEB_IP}
port=${WEB_PORT}

[BLUETOOTH]
" > ~/.remote-mpv-control/config.conf

chmod -R 750 "${PWD}/control"
chmod -R 750 "${PWD}/support"