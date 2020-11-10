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
    os.chdir(f"{CONFIG['GENERAL']['install_path']}/control")
    create_ipc_socket(CONFIG["GENERAL"]["ipc_socket"])
    # Optional - generate main (main.m3u) playlist if this option is present in configuration file
    if "PLAYLIST" in CONFIG:
        subprocess.call(f"{CONFIG['GENERAL']['install_path']}/control/playlists.py")
    # Run web based and bluetooth based interface
    WEBUI = subprocess.Popen(f"{CONFIG['GENERAL']['install_path']}/control/web.py")
    BLUE = subprocess.Popen(f"{CONFIG['GENERAL']['install_path']}/control/blue.py")
    # Run main mpv aplication
    subprocess.call([
        "mpv",
        f"--input-ipc-server={CONFIG['GENERAL']['ipc_socket']}",
        "--ytdl=no", # Necessary to improve switch time between playlist items
        "--fullscreen",
        "--fs-screen=all",
        "--loop=inf",
        "--hwdec=auto-safe",
        f"--sub-codepage=+{CONFIG['GENERAL']['subtitle_codepage']}",
        f"--playlist={CONFIG['GENERAL']['install_path']}/playlists/main.m3u"
        ])

        ])
    atexit.register(close_ui, webui=WEBUI, bluetooth=BLUE)
