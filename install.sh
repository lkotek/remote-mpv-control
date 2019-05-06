#!/bin/bash

IPC_SOCKET=/tmp/remote-mpv-control.sock
CONFIG_PATH=~/.remote-mpv-control
PLAYLIST_POSITION_PATH=/tmp/remote-mpv-playlist-pos
CURRENT_MODE=/tmp/remote-mpv-current-mode

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

mkdir $CONFIG_PATH

echo "[GENERAL]

install_path=${PWD}
ipc_socket=${IPC_SOCKET}
playlist_position_path=${PLAYLIST_POSITION_PATH}
current_mode=${CURRENT_MODE}
main_playlist_path=${PWD}/playlists/main.m3u

[WEB]

ip=${WEB_IP}
port=${WEB_PORT}

[BLUETOOTH]

# Section below is optional, uncomment if necessary

#[PLAYLIST]
#zapni_tv_url=
#zapni_tv_login=
#zapni_tv_password=
#sledovani_tv_url=
#sledovani_tv_login=
#sledovani_tv_password=
" > ~/.remote-mpv-control/config.conf

chmod -R 750 "${PWD}/control"
chmod -R 750 "${PWD}/support"