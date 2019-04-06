#!/usr/bin/env python3

""""Script providing functionality to control mpv player via web UI"""

import os
import common
from bottle import route, run, template, view, static_file, redirect, TEMPLATE_PATH

@route('/views/css/<filename>')
def server_static(filename):
    """Set path to serve the static files"""
    return static_file(filename, root=f"{PLAYER.cfg['GENERAL']['install_path']}/control/views/css")

@route('/start')
@view('start')
def start(position=0):
    """Main page of web UI with playlist loaded"""
    position = PLAYER.load_playlist_position()
    return template('start', playing=PLAYER.playlist[position], playlist=PLAYER.playlist)

@route('/play/<position>')
@view('play')
def play(position=0):
    """Jump to playlist position (program) selected by its number"""
    PLAYER.set_playlist_position(position)
    redirect("/start")

@route('/playlist/<key>')
@view('start')
def playlist(key=None):
    """Jump to next or previous playlist position"""
    PLAYER.switch_playlist_item(key)
    redirect("/start")

@route('/control/<key>')
@view('start')
def control(key=None):
    """Execute allowed (dict defined) remote control commands for mpv"""
    PLAYER.mpv_execute(key)
    redirect("/start")

@route('/window/screen')
@view('start')
def window():
    """Toggle between fulscreen and window"""
    PLAYER.mpv_execute("screen")
    redirect("/start")

@route('/volume/<change>')
@view('start')
def volume(change=None):
    """Volume control via pulseaudio"""
    PLAYER.change_volume(change)
    redirect("/start")

@route('/poweroff')
def poweroff():
    """Power of whole PC"""
    PLAYER.set_poweroff()
    redirect("/control/pause")

@route('/playeroff')
def playeroff():
    """Close mpv player only"""
    PLAYER.set_playeroff()
    exit(0)

@route('/sleep')
def sleep():
    """Pause player and put screen to sleep"""
    PLAYER.set_sleep()
    redirect("/control/pause")    

if __name__ == "__main__":
    PLAYER = common.BaseMpv()
    run(host=PLAYER.cfg['WEB']['ip'], port=PLAYER.cfg['WEB']['port'])
