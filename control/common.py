#!/bin/bash

"""Providing configuration for multiple scrispt"""

import configparser
import subprocess
import os

CONFIG = os.path.expanduser("~/.remote-mpv-control/config.conf")

def read_config():
    """Read main configuration file"""
    try:
        cfg = configparser.ConfigParser()
        cfg.read(CONFIG)
        return cfg
    except IOError as error:
        print("Cannot load configuration file: ", error)
        exit(1)

class BaseMpv():
    """Class to provide methods for common control of mpv player"""

    def __init__(self):
        """Configure default values"""
        self.cfg = read_config()
        self.playlist = None
        self.load_playlist()
        self.save_playlist_position()
        self.cmd_map = {
            "pause": "cycle pause",
            "prev": "playlist-prev",
            "next": "playlist-next",
            "screen": "cycle fullscreen"
            }
        # Set fullscreen and default volume at startup
        self.mpv_execute("screen")
        self.change_volume("default")        

    @classmethod
    def run_os_call(cls, command):
        """Wrapper of subprocess call"""
        subprocess.call(command)

    @classmethod
    def run_os_popen(cls, command):
        """Wrapper of popen cathing the output"""
        cmd_output = subprocess.Popen(
            command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
            )
        return str(cmd_output.communicate()[0])

    def set_sleep(self):
        """Pause playback and power off display"""
        self.run_os_call("xset -display :0.0 dpms force off")

    def set_poweroff(self):
        """Turn down whole system"""
        self.run_os_popen("sudo /sbin/shutdown -h now")

    def set_playeroff(self):
        """Turn down player only"""
        self.mpv_command("quit")

    def mpv_command(self, mpv_cmd):
        """Execute mpv command via socket"""
        subprocess.call(
            f"echo '{mpv_cmd}' | socat - {self.cfg['GENERAL']['ipc_socket']}",
            shell=True
            )

    def mpv_execute(self, key):
        """Execute mpv command by allowed key"""
        if key == "pause":
            self.show_text("Pauza / přehrát")
        self.mpv_command(self.cmd_map[key])

    def show_text(self, text):
        """Show text to mpv screen"""
        self.mpv_command(f'show-text \"{text}\"')

    def key_command(self, key_cmd):
        """Execute keypress to control mpv"""
        self.run_os_call(f"xdotool search --onlyvisible --class mpv key {key_cmd}")

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

    def switch_playlist_item(self, item):
        """Switch between items in playlist"""
        position = int(self.load_playlist_position())
        if item == "next":
            playlist_positon = position + 1 if position + 1 < len(self.playlist) else position
        elif item == "prev":
            playlist_positon = position - 1 if position - 1 >= 0 else position
        else:
            playlist_positon = position
        self.mpv_execute(item)
        self.show_text(self.playlist[playlist_positon])
        self.save_playlist_position(playlist_positon)

    def set_playlist_position(self, pos):
        """Set playlist position by number of item"""
        self.mpv_command(f"set playlist-pos {pos}")
        self.show_text(self.playlist[int(pos)])
        self.save_playlist_position(pos)

    def is_volume_muted(self):
        """Check if sink is muted"""
        volume = "pacmd list-sinks | grep muted | head -1 | cut -d: -f2"
        if "no" in self.run_os_popen(volume):
            return False
        return True

    def get_volume_info(self):
        """Realy not necessary to describe"""
        amixer = "amixer -R | grep 'Front Left: Playback' | cut -d[ -f2 | cut -d] -f1"
        return self.run_os_popen(amixer).replace("b", "").replace("\\n", "").replace("%", " %")

    def change_volume(self, change):
        """Change volume level via pactl"""
        if change == "up":
            operation = "+5%"
        elif change == "down":
            operation = "-5%"
        elif change == "default":
            operation = "40%"
        elif change == "mute":
            operation = "toggle"
            if self.is_volume_muted():
                self.show_text("Zapnout zvuk")
            else:
                self.show_text("Ztlumit zvuk")
            self.run_os_call(["pactl", "set-sink-mute", "0", operation])
        else:
            print("Wrong call :-(")
        self.run_os_call(["pactl", "set-sink-volume", "0", operation])
        if change != "mute":
            self.show_text(f"Hlasitost: {self.get_volume_info()}")
