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

window = ctk.CTk()

def anim_tick():
    dummy = 0

def playpause():
    if (playing):
        playing = False
    else:
        playing = True

DISPLAY_FRAME_SIZE = 400

def display_anim():
    return Image.open(os.path.join(r"C:\Program Files (x86)\Steam\steamapps\common\CrossCode\assets\media\entity\player\move.png")).crop([0, 0, 32, 32]).resize([DISPLAY_FRAME_SIZE, DISPLAY_FRAME_SIZE], Image.Resampling.NEAREST)

# Timer
timer = window.after(1000, anim_tick)

# Toolbar buttons
TOOLBAR_BTN_WIDTH = 100
TOOLBAR_BTN_HEIGHT = 100
load_btn = ctk.CTkButton(window, text="Load")
refresh_btn = ctk.CTkButton(window, text="Refresh")

# Control buttons
PLAYPAUSE_BTN_RELX = 0.5
PLAYPAUSE_BTN_RELY = 0.9
playpause_btn = ctk.CTkButton(window, text="Play/Pause", command=playpause)

FRAMECTRL_BTN_WIDTH = 30
#FRAMECTRL_BTN_HEIGHT = 30
backframe_btn = ctk.CTkButton(window, text="<", width=FRAMECTRL_BTN_WIDTH)
forwardframe_btn = ctk.CTkButton(window, text=">", width=FRAMECTRL_BTN_WIDTH)

playing = False

# Display frame

display_image = ctk.CTkImage(light_image=display_anim(), size=(DISPLAY_FRAME_SIZE, DISPLAY_FRAME_SIZE))
display_frame = ctk.CTkLabel(window, text='', width=DISPLAY_FRAME_SIZE, height=DISPLAY_FRAME_SIZE, image=display_image)


def load_ui():
    window.geometry('1000x700')
    window.title("cc-animation-viewer")


    playpause_btn.place(relx=PLAYPAUSE_BTN_RELX, rely=PLAYPAUSE_BTN_RELY, anchor=ctk.S)
    backframe_btn.place(relx=PLAYPAUSE_BTN_RELX - 0.1, rely=PLAYPAUSE_BTN_RELY, anchor=ctk.S)
    forwardframe_btn.place(relx=PLAYPAUSE_BTN_RELX + 0.1, rely=PLAYPAUSE_BTN_RELY, anchor=ctk.S)

    load_btn.place(relx=0.1, rely=0.05, anchor=ctk.N)
    refresh_btn.place(relx=0.25, rely=0.05, anchor=ctk.N)

    display_frame.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

    window.mainloop()



