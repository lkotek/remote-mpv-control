#!/usr/bin/env python3

"""Init mpv player script"""

import configparser
import subprocess
import atexit
import socket
import os

CONFIG = os.path.expanduser("~/.remote-mpv-control/config.conf")

def create_ipc_socket(sock):
    """Socket creation to control player"""
    mpv_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    try:
        os.remove(sock)
        mpv_socket.bind(sock)
    except OSError as error:
        print("Socket couldn't be created: ", error)

def close_ui(webui, blue):
    """Close all UI when player is closed"""
    webui.kill()
    blue.kill()

if __name__ == "__main__":
    try:
        CFG = configparser.ConfigParser()
        CFG.read(CONFIG)
    except IOError as error:
        print("Cannot load configuration file: ", error)
    create_ipc_socket(CFG["GENERAL"]["ipc_socket"])
    subprocess.Popen([
        "mpv",
        f"--input-ipc-server={CFG['GENERAL']['ipc_socket']}",
        "--playlist",
        f"{CFG['GENERAL']['install_path']}/playlists/main.m3u"
        ])
    WEBUI = subprocess.Popen([
        f"{CFG['GENERAL']['install_path']}/control/web.py",
        f"{CFG['WEB']['ip']}",
        f"{CFG['WEB']['port']}"
    ])
    BLUE = subprocess.Popen([f"{CFG['GENERAL']['install_path']}/control/bluetooth.py"])
    atexit.register(close_ui, webui=WEBUI, blue=BLUE)
