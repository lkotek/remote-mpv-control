#!/bin/bash

DEFAULT_WEB_IP="127.0.0.1"
DEFAULT_WEB_PORT=8081
DEFAULT_IPC_SOCKET="/tmp/remote-mpv-control-socket"

mkdir ~/.remote-mpv-control

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