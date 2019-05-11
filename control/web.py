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
    player_mode = PLAYER.load_current_mode()
    if player_mode == "iptv":
        return template(
                'start',
                playing=PLAYER.playlist[position],
                player=PLAYER,
                mode=player_mode
                )
    elif player_mode == "video":
        PLAYER.load_video_files()
        PLAYER.load_subtitle_files()
        PLAYER.load_video_directories()
        video = PLAYER.video[1] if PLAYER.video is not None else "Nevybráno"
        return template(
                'start',
                playing=video,
                player=PLAYER,
                mode=player_mode
                )

@route('/mode/<mode>')
@view('start')
def player_mode(mode="iptv"):
    """Toggle between IPTV, video and audio modes"""
    PLAYER.save_current_mode(mode)
    redirect("/start")

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

@route('/select_video/<selected>')
@view('play')
def select_video(selected=None):
    """Select video and jum to subtitle selection"""
    PLAYER.video = PLAYER.videos[selected]
    redirect("/start#selection")

@route('/select_subtitle/<selected>')
@view('play')
def select_subtitle(selected=None):
    """Select video and jum to subtitle selection"""
    PLAYER.subtitle = PLAYER.subtitles[selected]
    redirect("/start#selection")

@route('/select_dir/<selected>')
@view('play')
def select_dir(selected=None):
    """Select directory with video files"""
    PLAYER.video_dir = PLAYER.video_dirs[selected]
    redirect("/start#videos")

@route('/seek/<direction>')
@view('play')
def seek_video(direction=None):
    PLAYER.seek_video(direction)
    redirect("/start")

@route('/subtitle/<direction>')
@view('play')
def delay_subtitle(direction=None):
    PLAYER.delay_subtitle(direction)
    redirect("/start")

@route('/play_video')
@view('play')
def play_video(selected=None):
    """Play video with posibility of subtitle loaded"""
    PLAYER.mpv_command("playlist-clear")
    PLAYER.mpv_command("sub-remove")
    PLAYER.open_video(PLAYER.video[0])
    if PLAYER.subtitle:
        PLAYER.open_subtitle(PLAYER.subtitle[0])
    redirect("/start#top")

@route('/select_reset')
@view('play')
def select_reset():
    """Select video and jum to subtitle selection"""
    PLAYER.subtitle = None
    PLAYER.video = None
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

@route('/window/aspect')
@view('start')
def aspect():
    """Toggle between different aspect ratio settings"""
    PLAYER.mpv_execute("aspect")
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
