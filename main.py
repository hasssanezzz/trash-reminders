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

# parsing config
argumentList = sys.argv[1:]
LONG_OPTIONS = ["input-file", "sound-file"]
OPTIONS = "i:s:"

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
except getopt.error as err:
    print(str(err))


# reading file and parsing json
try:
    f = open(INPUT_SRC)
    data = json.load(f)
    f.close()
except:
    print("[!] Error: Can't find the data.json file")


def remind(every, name, message):
    while True:
        time.sleep(every * 60)
        os.system(SOUND_SRC)
        res = ctypes.windll.user32.MessageBoxW(0, message, name, 5)
        if res == 2:
            break

print("\n[*] ======= reminders initialized ======= \n")
for i in data:
    print(f"[+] Reminder '{i['name']}' created")
    x = Thread(target=remind, args=(i['every'], i['name'], i['message']))
    x.start()
