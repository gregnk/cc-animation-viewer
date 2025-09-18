'''
Copyright (c) 2025 Gregory Karastergios

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
'''

import json
import os
import string

from tkinter import filedialog

import util

cc_dir = ""
settings_json = ""

APP_VERSION = "0.1.0"
APP_DATE = "2025-XX-XX"

def load_settings_json():
    global cc_dir
    global settings_json

    settings_json = json.load(open("settings.json"))
    cc_dir = settings_json["cc_dir"]

def save_settings_json():
    global settings_json

    settings_json["cc_dir"] = cc_dir
    with open("settings.json", "w") as f:
        json.dump(settings_json, f)

# First Startup Code
##################################################

def check_first_startup():
    global settings_json

    print("settings_json[\"ran_first_startup\"] = " + str(settings_json["ran_first_startup"]))
    if (settings_json["ran_first_startup"] == False):
        check_common_dirs()
        settings_json["ran_first_startup"] = True
        save_settings_json()

def check_common_dirs():
    global cc_dir

    cc_dir_found = False

    if os.name == 'nt':
        for drive_letter in string.ascii_uppercase:
            check_path = drive_letter + ":\\Program Files (x86)\\Steam\\steamapps\\common\\CrossCode"
            print(check_path)
            if (os.path.isdir(check_path)):
                print("^^^^")
                cc_dir = check_path
                cc_dir_found = True
                break

    elif os.name == 'posix':
        if (os.path.isdir("~/.local/share/Steam/SteamApps/common/CrossCode/")):
            cc_dir = "~/.local/share/Steam/SteamApps/common/CrossCode/"
            cc_dir_found = True
    
    else:
        raise Exception("Unsupported OS")
    
    return cc_dir_found

# Settings UI Code
##################################################

def open_settings_dlg():
    # Temp Code
    # Dir selection currently taskes the place of the settings stuff
    # Internal var names will remain as-is
    select_cc_dir()

def select_cc_dir():
    global cc_dir
    directory_path = filedialog.askdirectory()

    if directory_path: 
        cc_dir = util.uniform_dir_slashes(util.escape_backslashes(directory_path))
        save_settings_json()
    else:
        print("Directory selection canceled.")