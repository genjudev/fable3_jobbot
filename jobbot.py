from win32 import win32gui # for pyinstaller
import win32ui, win32con, win32api
import cv2
import time
import sys
import pydirectinput
import d3dshot
import numpy
import traceback
from tkinter import *


def imageThere(images):
    img = d.get_latest_frame()
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    for i in images:
        res = cv2.matchTemplate(img_gray, i[0], cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        if max_val >= 0.8:
            return i[1]
    return None

HWND = win32gui.FindWindow(None, 'Fable 3')
win32gui.SetForegroundWindow(HWND)

x, y, x1, y1 = win32gui.GetClientRect(HWND)
x, y = win32gui.ClientToScreen(HWND, (x, y))
x1, y1 = win32gui.ClientToScreen(HWND, (x1 - x, y1 - y))
RAW_REGION = (x, y, x1, y1)
REGION = (x, int(y1*0.7), x1, y1)

print("""
        ----------------------------------------------------
        beep beep... showing image of what will be searched.
            """)

window = Tk()
window.overrideredirect(True)
window.wm_attributes("-topmost", True)
window.wm_attributes("-transparentcolor", "white")
window.attributes("-alpha", 0.3)
window.geometry('%ix%i+%i+%i' % (x1, int(y1*0.15), x, int(y1*0.9)))
display1 = Label(window)
display1.grid(row=1, column=0, padx=0, pady=0)
window.after(5000, window.quit)
window.mainloop()
window.destroy()

print("""
        ----------------------------------------------------
        beep beep... starting bot.
            """)

d = d3dshot.create(capture_output="numpy")

IMAGES = []

for i in ['src/img_1.PNG', 'src/img_2.PNG', 'src/img_3.PNG']:
    IMAGES.append(
        cv2.imread(i, 0)
        )

d.capture(region=REGION)
time.sleep(1)

try:
    while(True):

        try:
            keyCode=imageThere([
                [IMAGES[0], 1],
                [IMAGES[1], 2],
                [IMAGES[2], 3]
            ]
            )
            if(keyCode):
                pydirectinput.keyDown(str(keyCode))
                pydirectinput.keyUp(str(keyCode))
                continue
        except:
            tb=traceback.format_exc()
            print(tb)
            d.stop()
            break


        time.sleep(0.05)
except KeyboardInterrupt:
    d.stop()
    sys.exit()

d.stop()
