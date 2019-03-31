#!/bin/bash

DEFAULT_WEB_IP="127.0.0.1"
DEFAULT_WEB_PORT=8081
DEFAULT_IPC_SOCKET="/tmp/remote-mpv-control-socket"
CONFIG_PATH=~/.remote-mpv-control

if [ -d $CONFIG_PATH ]; then
    echo
    echo "Configuration already exists! If you want to create new one, run:"
    echo
    echo "rm -rf $CONFIG_PATH"
    echo
    exit 1
fi

read -p "Set IPv4 address for web UI: " DEFAULT_WEB_IP
read -p "Set port for web UI: " DEFAULT_WEB_PORT

mkdir $CONFIG_PATH

echo "[GENERAL]
install_path=${PWD}
ipc_socket=${DEFAULT_IPC_SOCKET}

[WEB]
ip=${DEFAULT_WEB_IP}
port=${DEFAULT_WEB_PORT}

[BLUETOOTH]
" > ~/.remote-mpv-control/config.conf

chmod -R 750 "${PWD}/control"
chmod -R 750 "${PWD}/support"