#!/bin/bash

"""Providing configuration for multiple scrispt"""

import configparser
import subprocess
import os

CONFIG = os.path.expanduser("~/.remote-mpv-control/config.conf")

MPV_COMMANDS_MAP = {
    "pause": "cycle pause",
    "prev": "playlist-prev",
    "next": "playlist-next",
    "fullscreen": "showfullscreen",
    "windowed": "showwindowed"
    }

def read_config():    
    try:
        cfg = configparser.ConfigParser()
        cfg.read(CONFIG)
        return cfg
    except IOError as error:
        print("Cannot load configuration file: ", error)
        exit(1)

def mpv_command(mpv_cmd):
    subprocess.call(f"echo {mpv_cmd} | socat - {CFG['GENERAL']['ipc_socket']}", shell=True)

def key_command(key_cmd):
    subprocess.call(["xdotool", "search", "--onlyvisible", "--class", "mpv", "key", key_cmd])
