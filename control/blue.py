#!/usr/bin/env python3

""""Script providing functionality to control mpv player via bluetooth Arduino based tool"""

import bluetooth
import time
import common

def execute(button):
    button_number = int(button)
    if button_number == 2:
        PLAYER.set_poweroff()

    elif button_number == 5:
        PLAYER.switch_playlist_item("prev")
    elif button_number == 4:
        PLAYER.mpv_execute("pause")
    elif button_number == 3:
        PLAYER.switch_playlist_item("next") 
           
    elif button_number == 8:        
        PLAYER.change_volume("down")
    elif button_number == 7:        
        PLAYER.change_volume("mute")
    elif button_number == 6:        
        PLAYER.change_volume("up")  

    elif button_number == 9:        
        PLAYER.mpv_execute("aspect")
    elif button_number == 10:        
        PLAYER.set_playeroff()
    elif button_number == 11:        
        PLAYER.mpv_execute("screen")
    return True

PORT = 1
CMD = ""

def search_remote_control():
    remote_controls = bluetooth.discover_devices()
    for address in remote_controls:
        if "HC-05" == bluetooth.lookup_name(address):
            print("Nalezeno: ", address)
            PLAYER.show_text("Blutooth ovladač nalezen.")
            return address
    return None

def connect_remote_control(address):
    socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    socket.connect((address, PORT))
    print("Onlajn")
    PLAYER.show_text("Blutooth ovladač připraven.")
    return socket 

remote_control = None
bluetooth_sock = None

if __name__ == "__main__":
    PLAYER = common.BaseMpv()
    while True:
        try:
            if remote_control == None:
                remote_control = search_remote_control()
                if remote_control != None:
                    bluetooth_sock = connect_remote_control(remote_control)
                else:
                    time.sleep(1)
                    continue
            data = bluetooth_sock.recv(32)
            cleaned_data = str(data).replace('\\r', '').replace('\\n', '').replace('b','').replace('\'', '')       
            if "*" in cleaned_data and "#" not in cleaned_data:
                CMD += cleaned_data
            elif "#" in cleaned_data:
                CMD += cleaned_data
                if execute(CMD.replace('*','').replace('#', '')):
                    bluetooth_sock.send("!")                
                else:
                    print("Error!")
                CMD = ""
        except bluetooth.btcommon.BluetoothError as e:
            print(e)
            PLAYER.show_text("Bluetooth ovladač spinká.")
            time.sleep(1)
            remote_control = None
            if bluetooth_sock != None: bluetooth_sock.close()
