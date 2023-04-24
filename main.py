import json
import time
from threading import Thread
import ctypes
import os
import sys
import getopt
import tkinter as tk
from tkinter import messagebox
import json
import tkinter.font as tkFont


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


# Define the GUI window
root = tk.Tk()
root.title("JSON CRUD Operation")
root.geometry("600x500")
# Function to add data to JSON file
def add_data():
    name = entry_name.get()
    message = entry_message.get()
    every = entry_every.get()

    # Validate input
    if name.strip() == '' or every.strip() == '':
        messagebox.showerror("Error", "Please enter name and message and duration.")
        return

    try:
        every = int(every)
    except ValueError:
        messagebox.showerror("Error", "duration must be a number.")
        return

    data = {"name": name, "message": message, "every": every}

    # Load existing data from JSON file
    with open("data.json", "r") as file:
        existing_data = json.load(file)

    # Append new data to existing data
    existing_data.append(data)

    # Write updated data to JSON file
    with open("data.json", "w") as file:
        json.dump(existing_data, file, indent=4)

    messagebox.showinfo("Success", "Data added successfully.")
    clear_entries()
    read_data()

def read_data():
    data_listbox.delete(0, tk.END)
    # Load data from JSON file
    with open("data.json", "r") as file:
        data = json.load(file)
        for item in data:
            data_listbox.insert(tk.END, f"Name: {item['name']}, Message: {item['message']}, every: {item['every']}")




def update_data():
    name = entry_name.get()
    message = entry_message.get()
    every = entry_every.get()

    # Validate input
    if name.strip() == '' or every.strip() == '':
        messagebox.showerror("Error", "Please enter name and duration.")
        return

    try:
        every = int(every)
    except ValueError:
        messagebox.showerror("Error", "duration must be a number.")
        return

    data = {"name": name, "message": message, "every": every}

    with open("data.json", "r") as file:
        existing_data = json.load(file)

    updated = False

    # Update data if name already exists, otherwise add new data
    for d in existing_data:
        if d["name"] == name:
            d["message"] = message
            d["every"] = every
            updated = True
            break

    if not updated:
        existing_data.append(data)

    with open("data.json", "w") as file:
        json.dump(existing_data, file, indent=4)

    messagebox.showinfo("Success", "Data updated successfully.")
    clear_entries()
    read_data()

def delete_data():
    name = entry_name.get()

    # Validate input
    if name.strip() == '':
        messagebox.showerror("Error", "Please enter name.")
        return

    with open("data.json", "r") as file:
        existing_data = json.load(file)

    # Remove data with given name
    existing_data = [d for d in existing_data if d["name"] != name]

    # Write updated data to JSON file
    with open("data.json", "w") as file:
        json.dump(existing_data, file, indent=4)

    messagebox.showinfo("Success", "Data deleted successfully.")
    clear_entries()
    read_data()

def clear_entries():
    entry_name.delete(0, tk.END)
    entry_message.delete(0, tk.END)
    entry_every.delete(0, tk.END)

# Create list

data_listbox=tk.Listbox(root)
data_listbox["borderwidth"] = "1px"
ft = tkFont.Font(family='Times',size=15)
data_listbox["font"] = ft
data_listbox["fg"] = "#333333"
data_listbox["justify"] = "center"
data_listbox.place(x=0,y=0,width=598,height=173)

read_data()
# Create input fields 


label_name=tk.Label(root)
ft = tkFont.Font(family='Times',size=10)
label_name["font"] = ft
label_name["fg"] = "#333333"
label_name["justify"] = "center"
label_name["text"] = "Name"
label_name.place(x=260,y=190,width=70,height=25)

entry_name=tk.Entry(root)
entry_name["borderwidth"] = "1px"
ft = tkFont.Font(family='Times',size=10)
entry_name["font"] = ft
entry_name["fg"] = "#333333"
entry_name["justify"] = "center"
entry_name["text"] = ""
entry_name.place(x=220,y=220,width=148,height=41)

label_message=tk.Label(root)
ft = tkFont.Font(family='Times',size=10)
label_message["font"] = ft
label_message["fg"] = "#333333"
label_message["justify"] = "center"
label_message["text"] = "Message"
label_message.place(x=260,y=270,width=70,height=25)
entry_message=tk.Entry(root)
entry_message["borderwidth"] = "1px"
ft = tkFont.Font(family='Times',size=10)
entry_message["font"] = ft
entry_message["fg"] = "#333333"
entry_message["justify"] = "center"
entry_message["text"] = ""
entry_message.place(x=220,y=300,width=148,height=42)

entry_every=tk.Entry(root)
entry_every["borderwidth"] = "1px"
ft = tkFont.Font(family='Times',size=10)
entry_every["font"] = ft
entry_every["fg"] = "#333333"
entry_every["justify"] = "center"
entry_every["text"] = ""
entry_every.place(x=220,y=380,width=148,height=43)
label_every=tk.Label(root)
ft = tkFont.Font(family='Times',size=10)
label_every["font"] = ft
label_every["fg"] = "#333333"
label_every["justify"] = "center"
label_every["text"] = "every"
label_every.place(x=260,y=350,width=70,height=25)

# Create buttons 


btn_add=tk.Button(root)
btn_add["bg"] = "#f0f0f0"
ft = tkFont.Font(family='Times',size=10)
btn_add["font"] = ft
btn_add["fg"] = "#000000"
btn_add["justify"] = "center"
btn_add["text"] = "Add"
btn_add.place(x=0,y=220,width=128,height=41)
btn_add["command"] = add_data

# btn_read=tk.Button(root)
# btn_read["bg"] = "#f0f0f0"
# btn_read["fg"] = "#000000"
# btn_read["justify"] = "center"
# btn_read["text"] = "Read"
# btn_read.place(x=220,y=430,width=148,height=43)
# btn_read["command"] = read_data


btn_update=tk.Button(root)
btn_update["bg"] = "#f0f0f0"
ft = tkFont.Font(family='Times',size=10)
btn_update["font"] = ft
btn_update["fg"] = "#000000"
btn_update["justify"] = "center"
btn_update["text"] = "Update"
btn_update.place(x=0,y=300,width=129,height=43)
btn_update["command"] = update_data

btn_delete=tk.Button(root)
btn_delete["bg"] = "#f0f0f0"
ft = tkFont.Font(family='Times',size=10)
btn_delete["font"] = ft
btn_delete["fg"] = "#000000"
btn_delete["justify"] = "center"
btn_delete["text"] = "Delete"
btn_delete.place(x=0,y=380,width=128,height=43)
btn_delete["command"] = delete_data

root.mainloop()