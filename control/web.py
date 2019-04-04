#!/usr/bin/env python3

import subprocess
import common
from bottle import route, run, template, view, static_file, redirect

# NEED TO REWRITE COMPLETELY

PLAYER = common.BaseMpv()

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
    PLAYER.set_playlist_position(position)
    redirect("/start")

@route('/playlist/<key>')
@view('start')
def playlist(key=None):
    PLAYER.switch_playlist_item(key)
    redirect("/start")

@route('/control/<key>')
@view('start')
def control(key=None):
    PLAYER.mpv_execute(key)
    redirect("/start")

@route('/window/screen')
@view('start')
def window():
    PLAYER.mpv_execute("screen")
    redirect("/start")

@route('/volume/<change>')
@view('start')
def volume(change=None):
    PLAYER.change_volume(change)
    redirect("/start")

@route('/poweroff')
def poweroff():
    PLAYER.set_poweroff()
    redirect("/control/pause")

@route('/playeroff')
def playeroff():
    PLAYER.set_playeroff()

@route('/sleep')
def sleep():
    PLAYER.key_command("p")
    PLAYER.set_sleep()
    subprocess.call()
    redirect("/start")

if __name__ == "__main__":
    run(host=PLAYER.cfg['WEB']['ip'], port=PLAYER.cfg['WEB']['port'])
