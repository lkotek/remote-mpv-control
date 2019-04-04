#!/usr/bin/env python3

"""Init mpv player script"""

import os
import subprocess
import atexit
import socket
import common

def create_ipc_socket(sock):
    """Socket creation to control player"""
    mpv_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    try:
        os.remove(sock)
        mpv_socket.bind(sock)
    except OSError as error:
        print("Socket couldn't be created: ", error)

def close_ui(webui, bluetooth):
    """Close all UI when player is closed"""
    webui.kill()
    bluetooth.kill()

if __name__ == "__main__":
    CONFIG = common.read_config()
    create_ipc_socket(CONFIG["GENERAL"]["ipc_socket"])
    WEBUI = subprocess.Popen([f"{CONFIG['GENERAL']['install_path']}/control/web.py"])
    BLUE = subprocess.Popen([f"{CONFIG['GENERAL']['install_path']}/control/bluetooth.py"])
    subprocess.call([
        "mpv",
        f"--input-ipc-server={CONFIG['GENERAL']['ipc_socket']}",
        "--playlist",
        f"{CONFIG['GENERAL']['install_path']}/playlists/main.m3u"
        ])
    atexit.register(close_ui, webui=WEBUI, bluetooth=BLUE)
