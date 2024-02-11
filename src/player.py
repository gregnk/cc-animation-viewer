'''
Copyright (c) 2024 Gregory Karastergios

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

import customtkinter as ctk
from PIL import Image
import os
import settings

from anim_json import load_anim_file, settings

window = ctk.CTk()

# Vars for the player state
class PlaybackControl:
    playing = False
    frame = 0

# The currently loaded anim file
class CurrentAnimFile:
    file_path = r"C:\Program Files (x86)\Steam\steamapps\common\CrossCode\assets\data\animations\player.json"
    sheets = ""
    animations = ""


# The animation which is currently playing
class CurrentAnim:
    index = 0

def load_anim_json():
    # Jank Code
    anim_file = load_anim_file(CurrentAnimFile.file_path)

    CurrentAnimFile.sheets = anim_file[0]
    CurrentAnimFile.animations = anim_file[1]

    # Update the selection combobox
    anim_name_list = []
    for anim in CurrentAnimFile.animations:
        anim_name_list.append(anim["name"])

    print(anim_name_list)
    anim_cmb.configure(values=anim_name_list)

def anim_tick():
    dummy = 0

def play_pause():
    if (PlaybackControl.playing):
        playpause_btn.configure(text="Play")
        PlaybackControl.playing = False

    else:
        playpause_btn.configure(text="Pause")
        PlaybackControl.playing = True

DISPLAY_FRAME_SIZE = 400

def get_display_image(anim_index):
    # Get the sheet name, and then get the path from the sheet json array
    # Temporarily set to the first one
    #load_anim_json()

    print(f"anim_index = {anim_index}")

    # Get the path of the sheet file
    current_sheet = CurrentAnimFile.sheets[CurrentAnimFile.animations[anim_index]["sheet"]]
    current_sheet_index = list(CurrentAnimFile.sheets.keys()).index(CurrentAnimFile.animations[anim_index]["sheet"])
    current_anim_sheet_src = current_sheet["src"] # The relative path in the JSON
    current_anim_sheet_path = settings.CC_DIR + "/assets/" + current_anim_sheet_src

    print(list(CurrentAnimFile.sheets.keys())[current_sheet_index])
    print(current_anim_sheet_path)

    # Crop the image and set the rendering params

    # The width and height defined by the sheet
    anim_width = current_sheet["width"]
    anim_height = current_sheet["height"]

    # The frame on the sheet that will be displayed
    frame = CurrentAnimFile.animations[anim_index]["frames"][0]

    # Crop coords (UNFINISHED)
    # (Probably doesn't work for all of them)
    left = anim_width * frame
    top = anim_height * frame
    right = anim_width * (frame + 1)
    bottom = anim_height * (frame + 1)

    light_image = Image.open(os.path.join(current_anim_sheet_path)) \
        .crop([left, top, right, bottom]) \
        .resize([DISPLAY_FRAME_SIZE, DISPLAY_FRAME_SIZE], Image.Resampling.NEAREST)

    return ctk.CTkImage(light_image=light_image, size=(DISPLAY_FRAME_SIZE, DISPLAY_FRAME_SIZE))

def get_anim_index_by_name(name):
    # Shit code, fix later
    index = 0
    for anim in CurrentAnimFile.animations:
        if (anim["name"] == name):
            return index
        
        index += 1

    return -1

def anim_combobox_handle(choice):
    print(choice)
    CurrentAnim.index = get_anim_index_by_name(choice) # Find a better way of doing this
    update_anim()

def update_anim():
    # Update the display image
    display_image = get_display_image(CurrentAnim.index)
    display_frame.configure(image=display_image)

# Timer
timer = window.after(1000, anim_tick)

# Toolbar buttons
TOOLBAR_BTN_WIDTH = 100
TOOLBAR_BTN_HEIGHT = 100
load_btn = ctk.CTkButton(window, text="Load")
refresh_btn = ctk.CTkButton(window, text="Refresh")
anim_cmb = ctk.CTkComboBox(window, values="", state="readonly", command=anim_combobox_handle)

# Control buttons
PLAYPAUSE_BTN_RELX = 0.5
PLAYPAUSE_BTN_RELY = 0.9
playpause_btn = ctk.CTkButton(window, text="Play", command=play_pause)

FRAMECTRL_BTN_WIDTH = 30
#FRAMECTRL_BTN_HEIGHT = 30
backframe_btn = ctk.CTkButton(window, text="<", width=FRAMECTRL_BTN_WIDTH)
forwardframe_btn = ctk.CTkButton(window, text=">", width=FRAMECTRL_BTN_WIDTH)

# Display frame
load_anim_json()
display_image = get_display_image(0)
display_frame = ctk.CTkLabel(window, text='', width=DISPLAY_FRAME_SIZE, height=DISPLAY_FRAME_SIZE, image=display_image)

def load_ui():
    
    window.geometry('1000x700')
    window.title("cc-animation-viewer")


    playpause_btn.place(relx=PLAYPAUSE_BTN_RELX, rely=PLAYPAUSE_BTN_RELY, anchor=ctk.S)
    backframe_btn.place(relx=PLAYPAUSE_BTN_RELX - 0.1, rely=PLAYPAUSE_BTN_RELY, anchor=ctk.S)
    forwardframe_btn.place(relx=PLAYPAUSE_BTN_RELX + 0.1, rely=PLAYPAUSE_BTN_RELY, anchor=ctk.S)

    load_btn.place(relx=0.1, rely=0.05, anchor=ctk.N)
    refresh_btn.place(relx=0.25, rely=0.05, anchor=ctk.N)
    anim_cmb.place(relx=0.40, rely=0.05, anchor=ctk.N)

    display_frame.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

    anim_cmb.set(CurrentAnimFile.animations[CurrentAnim.index]["name"])

    window.mainloop()
