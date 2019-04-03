#!/usr/bin/env python3

import subprocess
import common
from bottle import route, run, template, view, static_file, redirect

# NEED TO REWRITE COMPLETELY

PLAYER = common.BaseMpv()
FULLSCREEN = True

def volume_info():
    amixer = "amixer -R | grep 'Front Left: Playback' | cut -d[ -f2 | cut -d] -f1"
    cmd_output = subprocess.Popen(
        amixer, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
    return str(
        cmd_output.communicate()[0]
        ).replace("b", "").replace("\\n", "").replace("%", " %")

def is_volume_muted():
    amixer = "pacmd list-sinks | grep muted | cut -d: -f2"
    cmd_output = subprocess.Popen(
        amixer, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
    if "no" in str(cmd_output.communicate()[0]):
        return False
    return True

@route('/views/css/<filename>')
def server_static(filename):
    return static_file(filename, root=f"{PLAYER.cfg['GENERAL']['install_path']}/control/views/css")

@route('/start')
@view('start')
def start(position=0):
    position = PLAYER.load_playlist_position()
    return template('start', playing=PLAYER.playlist[position], playlist=PLAYER.playlist)

@route('/play/<position>')
@view('play')
def play(position=0):
    PLAYER.mpv_command(f"set playlist-pos {position}")
    PLAYER.mpv_command(f'show-text \"{PLAYER.playlist[int(position)]}\"')
    PLAYER.save_playlist_position(position)
    redirect("/start")

@route('/playlist/<key>')
@view('start')
def playlist(key=None):
    position = int(PLAYER.load_playlist_position())
    if key == "next":
        playlist_positon = position + 1 if position + 1 < len(PLAYER.playlist) else position
        PLAYER.key_command(">")
    elif key == "prev":
        playlist_positon = position - 1 if position - 1 >= 0 else position
        PLAYER.key_command("<")
    else:
        playlist_positon = position
    PLAYER.mpv_command(f'show-text \"{PLAYER.playlist[playlist_positon]}\"')
    PLAYER.save_playlist_position(playlist_positon)
    redirect("/start")

@route('/control/<key>')
@view('start')
def control(key=None):
    PLAYER.mpv_command(PLAYER.cmd_map[key])
    redirect("/start")

@route('/window/screen')
@view('start')
def window():
    PLAYER.key_command("f")
    redirect("/start")

@route('/volume/<change>')
@view('start')
def volume(change=None):
    if change == "up":
        operation = "5%+"
    elif change == "down":
        operation = "5%-"
    elif change == "mute":
        operation = "toggle"
        if is_volume_muted():
            PLAYER.mpv_command(f'show-text  \"Zapnout zvuk\"')
        else:
            PLAYER.mpv_command(f'show-text \"Ztlumit zvuk\"')
    else:
        print("Wrong call :-(")
    subprocess.call(["amixer", "-q", "sset", "Master", operation])
    if change != "mute":
        PLAYER.mpv_command(f'show-text \"Hlasitost: {(volume_info())}\"')
    redirect("/start")

@route('/poweroff')
def poweroff():
    subprocess.call(["sudo", "/sbin/shutdown", "-h", "now"])
    redirect("/pause")

@route('/playeroff')
def playeroff():
    subprocess.call([f"{PLAYER.cfg['GENERAL']['install_path']}/support/stop.sh"])

@route('/sleep')
def sleep():
    PLAYER.key_command("p")
    subprocess.call(["xset", "-display", ":0.0", "dpms", "force", "off"])
    redirect("/start")

if __name__ == "__main__":
    run(host=PLAYER.cfg['WEB']['ip'], port=PLAYER.cfg['WEB']['port'])
