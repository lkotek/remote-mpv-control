#!/bin/bash

"""Providing configuration for multiple scrispt"""

import configparser
import subprocess
import os

CONFIG = os.path.expanduser("~/.remote-mpv-control/config.conf")

class BaseMpv():
    def __init__(self):
        self.cfg = self.read_config()
        self.playlist = self.load_playlist()
        self.save_playlist_position(0)
        self.cmd_map = {
            "pause": "cycle pause",
            "prev": "playlist-prev",
            "next": "playlist-next"
            }

    def read_config(self):    
        try:
            config = configparser.ConfigParser()
            config.read(CONFIG)
            return config
        except IOError as error:
            print("Cannot load configuration file: ", error)
            exit(1)

    def mpv_command(self, mpv_cmd):
        subprocess.run(f"echo '{mpv_cmd}' | socat - {self.cfg['GENERAL']['ipc_socket']}", shell=True)

    def key_command(self, key_cmd):
        subprocess.run(["xdotool", "search", "--onlyvisible", "--class", "mpv", "key", key_cmd])       

    def load_playlist(self, selection=None):
        data = open(f"{self.cfg['GENERAL']['install_path']}/playlists/main.m3u")
        playlist = {}
        item_number = 0
        for line in data.readlines():
            if "EXTINF" in line:
                if not selection:
                    playlist.update({item_number:line.split(",")[1].strip()})
                else:
                    station_name = line.split(",")[1].strip()
                    if selection in station_name:
                        playlist.update({item_number:station_name})    
                item_number += 1            
        return playlist

    def save_playlist_position(self, pos):
        open("/tmp/remote-mpv-playlist-pos", "w").write(str(pos))

    def load_playlist_position(self):
        return open("/tmp/remote-mpv-playlist-pos", "r").read()       
