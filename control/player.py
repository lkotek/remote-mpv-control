#!/usr/bin/env python3

import subprocess
import socket
import json
import sys
import os

SOCKET = "/tmp/socket-mpv"
INSTALL = "/home/trilobyte/git/remote-mpv-control"
PLAYLIST = f"{INSTALL}/playlists/main.m3u"
CONFIG = f"{INSTALL}/control/config.json"

def load_config():
    try:
        return json.load(open(CONFIG))
    except IOError as e:
        print("Cannot load configuration file: ", e)

def create_ipc_socket():
    mpv_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    try:
        os.remove(SOCKET)
        mpv_socket.bind(SOCKET)
    except OSError as e:
        print("Socket couldn't be created: ", e)    

if __name__ == "__main__":
    create_ipc_socket()
    config = load_config()
    for script in config["control_scripts"]:
        os.chmod(f"{INSTALL}/control/{script}", 0o750)
    subprocess.call([
        "mpv",
        f"--input-ipc-server={SOCKET}",
        "--playlist",
        PLAYLIST
        ])
    subprocess.call([f"{INSTALL}/control/web.py", config["web_ip"], config["web_port"]])
    subprocess.call([f"{INSTALL}/control/bluetooth.py"])
    