#!/usr/bin/env python3

from bottle import route, run, template, view, static_file, redirect, SimpleTemplate
import subprocess
import config
import socket
import sys

# NEED TO REWRITE COMPLETELY

CFG = config.read_config()
FULLSCREEN = True

def volume_info():
    a = "amixer -R | grep 'Front Left: Playback' | cut -d[ -f2 | cut -d] -f1"
    i = subprocess.Popen(a,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    return str(i.communicate()[0]).replace("b","").replace("\\n","").replace("%", " %")

@route('/views/css/<filename>')
def server_static(filename):
    return static_file(filename, root=f"{CFG['GENERAL']['install_path']}/control/views/css")

@route('/start')
@route('/start/<selection>')
@view('start')
def start(playing=None, selection=None):  
    config.mpv_command("set playlist-pos 0")      
    return template('start', playing="XXX", playlist={"x": "xx", "xx":"xxxx"})

@route('/play/<key>')
@view('start')
def play(key=None):
    config.mpv_command(config.MPV_COMMANDS_MAP[key])
    redirect("/start")

@route('/window/screen')
@view('start')
def window(screen=None):
    config.key_command("f")
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
        config.mpv_command(f"show-text Ztlumit")
    else:
        print("Wrong call :-(")
    subprocess.call(["amixer", "-q", "sset", "Master", operation])
    if change != "mute":
        config.mpv_command(f"show-text {(volume_info())}")
    redirect("/start") 

@route('/poweroff')
def poweroff(change=None):
    subprocess.call(["sudo", "/sbin/shutdown", "-h", "now"])
    redirect("/pause")

@route('/playeroff')
def playeroff(change=None):
    subprocess.call([f"{CFG['GENERAL']['install_path']}/support/stop.sh"])

@route('/sleep')
def sleep(change=None):
    config.key_command("p")
    subprocess.call(["xset", "-display", ":0.0", "dpms", "force", "off"])
    redirect("/start")

if __name__ == "__main__":
    run(host=CFG['WEB']['ip'], port=CFG['WEB']['port'])