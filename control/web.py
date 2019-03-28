#!/usr/bin/env python3

from bottle import route, run, template, view, static_file, redirect, SimpleTemplate
import subprocess
import socket
import sys

# NEED TO REWRITE COMPLETELY

WEB_DIR = sys.argv[3]
IPC_SOCKET = sys.argv[4]

def command(cmd):
    subprocess.call(f"echo {cmd} | socat - {IPC_SOCKET}", shell=True)

def volume_info():
    a = "amixer -R | grep 'Front Left: Playback' | cut -d[ -f2 | cut -d] -f1"
    i = subprocess.Popen(a,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    return str(i.communicate()[0]).replace("b","").replace("\\n","").replace("%", " %")

def notification(msg):
    cmd = "echo {0} | osd_cat -p top -A center -d 1 -o 900 -c WHITE -s 3 -f -cronyx-*-medium-*-*-*-*-240-100-100-*-*-*-*".format(msg)
    subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)

@route('/views/css/<filename>')
def server_static(filename):
    return static_file(filename, root=WEB_DIR +'/views/css')

@route('/start')
@route('/start/<selection>')
@view('start')
def start(playing=None, selection=None):    
    pass
    #return template('start', playing=playlist[player.playlist_pos], playlist=new_playlist, forward=fwrd, backward=bcrd)

@route('/play/<p_id>')
@view('start')
def play(p_id=None):
    redirect("/start")    

@route('/key/<operation>')
#@view('start')
def keypress(operation=None):
    #subprocess.call(["xdotool", "key", operation])
    command("cycle pause")
    #redirect("/start")

@route('/volume/<change>')
@view('start')
def volume(change=None):
    if change == "up":
        operation = "5%+"
    elif change == "down":
        operation = "5%-"
    elif change == "mute":
        operation = "toggle"
        notification("Ztlumit")
    else:
        print("Wrong call :-(")
    subprocess.call(["amixer", "-q", "sset", "Master", operation])
    if change != "mute":
        notification(volume_info())
    redirect("/start") 

@route('/poweroff')
def poweroff(change=None):
    subprocess.call(["sudo", "/sbin/shutdown", "-h", "now"])
    redirect("/pause")

@route('/playeroff')
def playeroff(change=None):
    subprocess.call([WEB_DIR + "/stop.sh"])

@route('/sleep')
def sleep(change=None):
    subprocess.call(["xdotool", "key", "p"])
    subprocess.call(["xset", "-display", ":0.0", "dpms", "force", "off"])
    redirect("/start")

if __name__ == "__main__":
    run(host="127.0.0.1", port=8081)