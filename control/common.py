#!/bin/bash

"""Providing configuration for multiple scrispt"""

import configparser
import subprocess
import os

CONFIG = os.path.expanduser("~/.remote-mpv-control/config.conf")

class BaseMpv():
    """Class to provide configuration and define methods for common use"""
    def __init__(self):
        """Configure default values"""
        self.cfg = None
        self.playlist = None
        self.read_config()
        self.load_playlist()
        self.save_playlist_position()
        self.cmd_map = {
            "pause": "cycle pause",
            "prev": "playlist-prev",
            "next": "playlist-next"
            }
    def read_config(self):
        """Read main configuration file"""
        try:
            self.cfg = configparser.ConfigParser()
            self.cfg.read(CONFIG)
        except IOError as error:
            print("Cannot load configuration file: ", error)
            exit(1)
    def mpv_command(self, mpv_cmd):
        """Execute mpv command via socket"""
        subprocess.run(
            f"echo '{mpv_cmd}' | socat - {self.cfg['GENERAL']['ipc_socket']}",
            shell=True
            )
    @staticmethod
    def key_command(key_cmd):
        """Execute keypress to control mpv"""
        subprocess.run(["xdotool", "search", "--onlyvisible", "--class", "mpv", "key", key_cmd])
    def load_playlist(self, selection=None):
        """Load playlist data from main playlist file"""
        data = open(f"{self.cfg['GENERAL']['install_path']}/playlists/main.m3u")
        self.playlist = {}
        item_number = 0
        for line in data.readlines():
            if "EXTINF" in line:
                if not selection:
                    self.playlist.update({item_number:line.split(",")[1].strip()})
                else:
                    station_name = line.split(",")[1].strip()
                    if selection in station_name:
                        self.playlist.update({item_number:station_name})
                item_number += 1
    def save_playlist_position(self, pos=0):
        """Save position in current plalist"""
        try:
            open(self.cfg['GENERAL']['playlist_position_path'], "w").write(str(pos))
        except IOError as error:
            print(error)
            exit(1)
    def load_playlist_position(self):
        """Load current playlist position"""
        try:
            return int(open(self.cfg['GENERAL']['playlist_position_path'], "r").read())
        except IOError as error:
            print(error)
            exit(1)
