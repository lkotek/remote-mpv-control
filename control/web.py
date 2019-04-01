#!/usr/bin/env python3

from bottle import route, run, template, view, static_file, redirect, SimpleTemplate
import subprocess
import common
import socket
import sys

# NEED TO REWRITE COMPLETELY

main = common.BaseMpv()
FULLSCREEN = True

def volume_info():
    a = "amixer -R | grep 'Front Left: Playback' | cut -d[ -f2 | cut -d] -f1"
    i = subprocess.Popen(a,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    return str(i.communicate()[0]).replace("b","").replace("\\n","").replace("%", " %")

@route('/views/css/<filename>')
def server_static(filename):
    return static_file(filename, root=f"{main.cfg['GENERAL']['install_path']}/control/views/css")

@route('/start')
@view('start')
def start(playing=None, position=0):      
    return template('start', playing=main.playlist[int(position)], playlist=main.playlist)

@route('/play/<position>')
@view('play')
def play(playing=None, position=0):     
    main.mpv_command(f"set playlist-pos {position}") 
    main.mpv_command(f"show-text '{main.playlist[int(position)]}'") 
    main.save_playlist_position(position)      
    redirect("/start")

@route('/control/<key>')
@view('start')
def control(key=None):
    main.mpv_command(main.cmd_map[key])
    position = main.load_playlist_position()
    main.mpv_command(f"show-text '{main.playlist[int(position)]}'") 
    redirect("/start")

@route('/window/screen')
@view('start')
def window(screen=None):
    main.key_command("f")
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
        main.mpv_command(f"show-text Ztlumit")
    else:
        print("Wrong call :-(")
    subprocess.call(["amixer", "-q", "sset", "Master", operation])
    if change != "mute":
        main.mpv_command(f"show-text {(volume_info())}")
    redirect("/start") 

@route('/poweroff')
def poweroff(change=None):
    subprocess.call(["sudo", "/sbin/shutdown", "-h", "now"])
    redirect("/pause")

@route('/playeroff')
def playeroff(change=None):
    subprocess.call([f"{main.cfg['GENERAL']['install_path']}/support/stop.sh"])

@route('/sleep')
def sleep(change=None):
    main.key_command("p")
    subprocess.call(["xset", "-display", ":0.0", "dpms", "force", "off"])
    redirect("/start")

if __name__ == "__main__":
    run(host=main.cfg['WEB']['ip'], port=main.cfg['WEB']['port'])