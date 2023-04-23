import json
import time
from threading import Thread
import ctypes
import os
import sys
import getopt


# Configurations
SOUND_SRC = "c:/Windows/Media/notify.wav"
INPUT_SRC = "data.json"
NOTIFICATION = False

# parsing config
argumentList = sys.argv[1:]
OPTIONS = "ni:s:"
LONG_OPTIONS = ["input-file", "sound-file", "notification"]

# parsed json
data = {}

# paring command line arguments
try:
    arguments, values = getopt.getopt(argumentList, OPTIONS, LONG_OPTIONS)
    for currentArgument, currentValue in arguments:
        if currentArgument in ("-i", "--i"):
            print(f"[*] Getting input from ({currentValue})")
            INPUT_SRC = currentValue
        elif currentArgument in ("-s", "--sound-file"):
            print(f"[*] Getting sound file from ({currentValue})")
            SOUND_SRC = currentValue
        elif currentArgument in ("-n", "--notification"):
            print(f"[*] Getting sound file from ({currentValue})")
            NOTIFICATION = True

            try:
                from plyer import notification
            except ImportError:
                print("[!] Error in importing the 'plyer' module")
                NOTIFICATION = False
                
except getopt.error as err:
    print(str(err))


# reading file and parsing json
try:
    f = open(INPUT_SRC)
    data = json.load(f)
    f.close()
except:
    print(f"[!] Error: Can't open the {INPUT_SRC} file.")


def remind_message_box(every, name, message):
    while True:
        time.sleep(every * 60)
        try:
            os.system(SOUND_SRC)
        except:
            print(f"[!] Error: Can't open sound file from {SOUND_SRC}.")
        res = ctypes.windll.user32.MessageBoxW(0, message, name, 5)
        if res == 2:
            break


def remind_notification(every, name, message):
    while True:
        time.sleep(every * 60)
        notification.notify(
            title=f'Reminder - {name}',
            message=message,
            app_icon=None,
            timeout=1,
        )


print("\n[*] ======= reminders initialized ======= \n")
for i in data:
    print(f"[+] Reminder '{i['name']}' created")
    if NOTIFICATION:
        x = Thread(target=remind_notification, args=(
            i['every'], i['name'], i['message']))
    else:
        x = Thread(target=remind_message_box, args=(
            i['every'], i['name'], i['message']))
    x.start()
    print()
