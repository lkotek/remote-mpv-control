#!/usr/bin/env python3

"""Optional script to generate playlist from sledovani.tv and zapni_req.tv IPTV providers"""

from urllib.parse import urlencode
from io import BytesIO
from requests.auth import HTTPBasicAuth
import requests
import pycurl
import common

def get_zapnitv_plalist():
    """Authorize and get m3u playlist from zapni.tv via curl"""
    cookie = f"{PLAYLIST_PATH}/zapnitv.cookie"
    zapni_req = pycurl.Curl()
    zapni_req.setopt(pycurl.URL, f"{CONFIG['PLAYLIST']['zapni_tv_url']}/sign/in")
    login_data = {
        "username": CONFIG["PLAYLIST"]["zapni_tv_login"],
        "password": CONFIG["PLAYLIST"]["zapni_tv_password"],
        "do": "signInForm-form-submit",
        "send": "Přihlásit se"
        }
    login_data_encoded = urlencode(login_data)
    zapni_req.setopt(pycurl.POSTFIELDS, login_data_encoded)
    zapni_req.setopt(pycurl.COOKIEJAR, cookie)
    zapni_req.perform()
    # Get playlist after previous authorization
    buffer = BytesIO()
    zapni_req.setopt(pycurl.URL, f"{CONFIG['PLAYLIST']['zapni_tv_url']}/tv/playlist.m3u")
    zapni_req.setopt(pycurl.COOKIEFILE, cookie)
    zapni_req.setopt(pycurl.WRITEDATA, buffer)
    zapni_req.perform()
    zapni_req.close()
    return buffer.getvalue().decode('utf-8')

def get_sledovanitv_playlist():
    """Authorize and get m3u playlist from sledovanitv.cz"""
    return requests.get(
        f"{CONFIG['PLAYLIST']['sledovani_tv_url']}/vlc/playlist",
        auth=HTTPBasicAuth(
            CONFIG['PLAYLIST']['sledovani_tv_login'],
            CONFIG['PLAYLIST']['sledovani_tv_password']
            )
        ).text

def save_playlist(playlist_prefix, playlist):
    """Save m3u playlist file created from dictionary"""
    try:
        with open(f"{PLAYLIST_PATH}/playlist-{playlist_prefix}.m3u", "w") as file:
            for _, playlist_value in playlist.items():
                file.write(f"{playlist_value}\n")
    except IOError as error:
        print("Cannot save playlist: ", error)
        exit(1)

def save_allowed_playlists_keys(playlist_list):
    """Save allowed keys for playlist dict items to file"""
    for playlist in playlist_list:
        try:
            with open(ALLOWED_KEYS, "w") as file:
                file.write("#EXTM3U\n")
                for key in playlist:
                    file.write(f"{key}\n")
        except IOError as error:
            print("Cannot write to allowed keys file: ", error)
            exit(1)

def create_playlist_from_keys(keys_file, playlist_save_file, playlist_dict):
    """Create m3u playlist file based on playlist dict with allowed keys"""
    try:
        keys = [k.strip() for k in open(keys_file, 'r').readlines()]
    except IOError as error:
        print("Cannot open keys file: ", error)
        exit(1)
    try:
        with open(playlist_save_file, "w") as file:
            file.write("#EXTM3U\n")
            for key in keys:
                try:
                    file.write(f"{playlist_dict[key]}\n")
                except KeyError as error:
                    print("Cannot find key: ", error)
                    exit(1)
    except IOError as error:
        print("Cannot empty target playlist file: ", error)
        exit(1)

def parse_m3u_playlist(key_prefix, data):
    """Parse m3u playlist file and create dictionary based on it"""
    programs = {}
    for item in data.split("#"):
        if "EXTINF" not in item:
            continue
        key = item.split(",")[1].split("http")[0].strip().lower().replace(" ", "-")
        if "nepřístupný" not in key: # Skip disabled items from m3u playlist
            programs.update({f"{key_prefix}-{key}": f"#{item}"})
    return programs

if __name__ == "__main__":
    CONFIG = common.read_config()
    PLAYLIST_PATH = f"{CONFIG['GENERAL']['install_path']}/playlists"
    ALLOWED_KEYS = f"{PLAYLIST_PATH}/playlist-allowed-keys.txt"
    SELECTED_KEYS = f"{PLAYLIST_PATH}/playlist-selected-keys.txt"
    # Get playlist from multiple providers if available
    PLAYLISTS = []
    if "zapni_tv_url" in CONFIG["PLAYLIST"]:
        PREFIX = "zapnitv"
        ZAPNI = get_zapnitv_plalist()
        ZAPNI_PARSED = parse_m3u_playlist(PREFIX, ZAPNI)
        save_playlist(PREFIX, ZAPNI_PARSED)
        PLAYLISTS.append(ZAPNI_PARSED)
    if "sledovani_tv_url" in CONFIG["PLAYLIST"]:
        PREFIX = "sledovanitv"
        SLEDOVANI = get_sledovanitv_playlist()
        SLEDOVANI_PARSED = parse_m3u_playlist(PREFIX, SLEDOVANI)
        save_playlist(PREFIX, SLEDOVANI_PARSED)
        PLAYLISTS.append(SLEDOVANI_PARSED)
    # Create one combined playlist from multiple providers with *allowed* items only
    save_allowed_playlists_keys(PLAYLISTS)
    COMBINED = {}
    for p_dic in PLAYLISTS:
        COMBINED = {**COMBINED, **p_dic}
    create_playlist_from_keys(
        SELECTED_KEYS,
        CONFIG['GENERAL']['main_playlist_path'],
        COMBINED
        )
