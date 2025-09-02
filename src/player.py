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

import customtkinter as ctk
from PIL import Image
import os
import settings

from anim_json import load_anim_file, settings
import util

window = ctk.CTk()

# Vars for the player state
class PlaybackControl:
    playing = False
    loop = True
    frame = 0
    direction = 0

# The currently loaded anim file
class CurrentAnimFile:
    file_path = r"C:\Program Files (x86)\Steam\steamapps\common\CrossCode\assets\data\animations\player.json" # Temporary code
    sheets = ""
    animations = ""


# The animation which is currently playing
class CurrentAnim:
    index = 0
    data = ""

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
    anim_cmb.set(CurrentAnimFile.animations[CurrentAnim.index]["name"])
    PlaybackControl.frame = 0

def load_file_dlg():
    load_file_path = ctk.filedialog.askopenfilename(
        title = "Select JSON file", 
        initialdir = settings.CC_DIR + util.uniform_dir_slashes("/assets/data/animations"),
        filetypes = [("JSON File", "*.json"), ("All files", "*.*")])
    
    if (load_file_path != ""):
        CurrentAnimFile.file_path = load_file_path
    
        load_anim_json()
        update_anim()

def anim_tick():
    if (PlaybackControl.playing):
        if (PlaybackControl.frame < len(CurrentAnimFile.animations[CurrentAnim.index]["frames"]) - 1):
            PlaybackControl.frame += 1

        else:

            if (PlaybackControl.loop):
                PlaybackControl.frame = 0

            else:
                pause()

        
        update_anim()

    # Not sure if this will cause a stackoverflow
    window.after(100, anim_tick) 

def play_pause():
    if (PlaybackControl.playing):
        pause()

    else:

        # Restart if at the end of the anim and looping is off
        if (PlaybackControl.loop == False and PlaybackControl.frame == len(CurrentAnimFile.animations[CurrentAnim.index]["frames"]) - 1):
            PlaybackControl.frame = 0

        play()

    

def play():
    playpause_btn.configure(text="Pause")
    PlaybackControl.playing = True

def pause():
    playpause_btn.configure(text="Play")
    PlaybackControl.playing = False

def back_frame():
    if (PlaybackControl.playing == False):
        if (PlaybackControl.frame > 0):
            PlaybackControl.frame -= 1
            update_anim()

def forward_frame():
    if (PlaybackControl.playing == False):
        if (PlaybackControl.frame < len(CurrentAnimFile.animations[CurrentAnim.index]["frames"]) - 1):
            PlaybackControl.frame += 1
            update_anim()

def toggle_loop():
    if (PlaybackControl.loop == True):
        PlaybackControl.loop = False
    
    elif (PlaybackControl.loop == False):
        PlaybackControl.loop = True

    else:
        print("toggle_loop() error: Not bool")


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
    print(util.uniform_dir_slashes(current_anim_sheet_path))
    print(f"current_sheet[\"offX\"] = {str(current_sheet["offX"])}")
    print(f"current_sheet[\"offY\"] = {str(current_sheet["offY"])}")

    # Crop the image and set the rendering params

    # The width and height defined by the sheet
    anim_width = current_sheet["width"]
    anim_height = current_sheet["height"]

    # The frame on the sheet that will be displayed
    anim_frame = CurrentAnimFile.animations[anim_index]["frames"][PlaybackControl.frame]
    print(f"PlaybackControl.frame = {PlaybackControl.frame}")
    print(f"anim_frame = {anim_frame}")
    print(f"CurrentAnim.animations[anim_index][\"frames\"] = {CurrentAnimFile.animations[anim_index]["frames"]}")

    # Crop coords (UNFINISHED)
    # TODO: Add tile offsets

    left = anim_width * anim_frame + current_sheet["offX"]
    top = 0 + (anim_height * PlaybackControl.direction) + current_sheet["offY"]
    right = anim_width * (anim_frame + 1) + current_sheet["offX"]
    bottom = anim_height + (anim_height * PlaybackControl.direction) + current_sheet["offY"]

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

# What happens when the animation is changed
def anim_cmb_handle(choice):
    pause()
    print(choice)

    anim_index_old = CurrentAnim.index
    CurrentAnim.index = get_anim_index_by_name(choice) # Find a better way of doing this
    CurrentAnim.data = CurrentAnimFile.animations[CurrentAnim.index]
    
    # Reset frame
    PlaybackControl.frame = 0
    
    # Reset current direction index if the new anim a different same amount
    if (CurrentAnimFile.animations[CurrentAnim.index]["dirs"] != CurrentAnimFile.animations[anim_index_old]["dirs"]):
        PlaybackControl.direction = 0
    

    direction_input.delete(0, 100)
    direction_input.insert(0, "0")
    update_anim()

def direction_input_handle(input):
    dir_input_int = int(direction_input.get())
    if (dir_input_int < CurrentAnimFile.animations[CurrentAnim.index]["dirs"]):
        PlaybackControl.direction = dir_input_int
        update_anim()

def frame_input_handle(input):
    framenbr_input_int = int(framenbr_input.get())
    if (PlaybackControl.playing == False):
        if (framenbr_input_int >= 0 and framenbr_input_int < len(CurrentAnimFile.animations[CurrentAnim.index]["frames"])):
            PlaybackControl.frame = framenbr_input_int
            update_anim()


def update_anim():
    # Update the display image
    display_image = get_display_image(CurrentAnim.index)
    display_frame.configure(image=display_image)

    framenbr_input.delete(0, ctk.END)
    framenbr_input.insert(0, PlaybackControl.frame)

    update_ctrl_lbls()

def open_settings_dlg():
    dummy = 0

# Timer
window.after(800, anim_tick)

# Toolbar buttons
TOOLBAR_BTN_WIDTH = 100
TOOLBAR_BTN_HEIGHT = 100
load_btn = ctk.CTkButton(window, text="Load", command=load_file_dlg)
refresh_btn = ctk.CTkButton(window, text="Refresh", command=load_anim_json)
anim_cmb = ctk.CTkComboBox(window, values="", state="readonly", command=anim_cmb_handle)
settings_btn = ctk.CTkButton(window, text="Settings", command=open_settings_dlg)

# Control buttons
PLAYPAUSE_BTN_RELX = 0.5
PLAYPAUSE_BTN_RELY = 0.9
playpause_btn = ctk.CTkButton(window, text="Play", command=play_pause)

FRAMECTRL_BTN_WIDTH = 30
#FRAMECTRL_BTN_HEIGHT = 30
backframe_btn = ctk.CTkButton(window, text="<", width=FRAMECTRL_BTN_WIDTH, command=back_frame)
forwardframe_btn = ctk.CTkButton(window, text=">", width=FRAMECTRL_BTN_WIDTH, command=forward_frame)

loop_chk = ctk.CTkCheckBox(window, text="Loop", command=toggle_loop)
loop_chk.select()

FRAMECTRL_FIELD_WIDTH = 30
direction_lbl = ctk.CTkLabel(window, text="Direction", width=FRAMECTRL_FIELD_WIDTH)
direction_input = ctk.CTkEntry(window, width=FRAMECTRL_FIELD_WIDTH)
direction_len_lbl = ctk.CTkLabel(window, text="/", width=FRAMECTRL_FIELD_WIDTH)

framenbr_lbl = ctk.CTkLabel(window, text="Frame", width=FRAMECTRL_FIELD_WIDTH)
framenbr_input = ctk.CTkEntry(window, width=FRAMECTRL_FIELD_WIDTH)
framenbr_len_lbl = ctk.CTkLabel(window, text="/", width=FRAMECTRL_FIELD_WIDTH)

def update_ctrl_lbls():
    print(CurrentAnimFile.animations[CurrentAnim.index]["dirs"])
    direction_len_lbl.configure(text="/ " + str(int(CurrentAnimFile.animations[CurrentAnim.index]["dirs"]) - 1))
    framenbr_len_lbl.configure(text="/ " + str(len(CurrentAnimFile.animations[CurrentAnim.index]["frames"]) - 1))


# Display frame
load_anim_json()
display_image = get_display_image(0)
display_frame = ctk.CTkLabel(window, text='', width=DISPLAY_FRAME_SIZE, height=DISPLAY_FRAME_SIZE, image=display_image)

def load_ui():
    
    window.geometry('1000x700')
    window.title("cc-animation-viewer")

    # Playback controls
    playpause_btn.place(relx=PLAYPAUSE_BTN_RELX, rely=PLAYPAUSE_BTN_RELY, anchor=ctk.S)
    backframe_btn.place(relx=PLAYPAUSE_BTN_RELX - 0.1, rely=PLAYPAUSE_BTN_RELY, anchor=ctk.S)
    forwardframe_btn.place(relx=PLAYPAUSE_BTN_RELX + 0.1, rely=PLAYPAUSE_BTN_RELY, anchor=ctk.S)
    loop_chk.place(relx=PLAYPAUSE_BTN_RELX - 0.065, rely=PLAYPAUSE_BTN_RELY + 0.0559, anchor=ctk.S)

    # Direction
    direction_lbl.place(relx=PLAYPAUSE_BTN_RELX - 0.35, rely=PLAYPAUSE_BTN_RELY, anchor=ctk.S)
    direction_input.insert(0, "0")
    direction_input.bind("<Return>", direction_input_handle) # TODO: Have this update on input as opposed to requiring enter
    direction_input.place(relx=PLAYPAUSE_BTN_RELX - 0.3, rely=PLAYPAUSE_BTN_RELY, anchor=ctk.S)
    direction_len_lbl.place(relx=PLAYPAUSE_BTN_RELX - 0.27, rely=PLAYPAUSE_BTN_RELY, anchor=ctk.S)

    # Frame
    framenbr_lbl.place(relx=PLAYPAUSE_BTN_RELX - 0.35, rely=PLAYPAUSE_BTN_RELY + 0.06, anchor=ctk.S)
    framenbr_input.insert(0, "0")
    framenbr_input.bind("<Return>", frame_input_handle) # TODO: Have this update on input as opposed to requiring enter
    framenbr_input.place(relx=PLAYPAUSE_BTN_RELX - 0.3, rely=PLAYPAUSE_BTN_RELY + 0.06, anchor=ctk.S)
    framenbr_len_lbl.place(relx=PLAYPAUSE_BTN_RELX - 0.27, rely=PLAYPAUSE_BTN_RELY + 0.06, anchor=ctk.S)

    update_ctrl_lbls()

    # Top bar
    load_btn.place(relx=0.1, rely=0.05, anchor=ctk.N)
    refresh_btn.place(relx=0.25, rely=0.05, anchor=ctk.N)
    anim_cmb.place(relx=0.40, rely=0.05, anchor=ctk.N)
    settings_btn.place(relx=0.90, rely=0.05, anchor=ctk.N)

    # Animation display frame
    display_frame.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

    window.mainloop()