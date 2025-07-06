import cv2
import numpy as np
import pyautogui
import pyautogui as pg
from pathlib import Path
import pytesseract
from PIL import ImageGrab, ImageDraw
import time
import platform
import pygetwindow as gw
BASE_DIR = Path(__file__).resolve().parent.parent

def move_mouse(x,y):
    os_name = platform.system()
    if os_name == 'Darwin':
        scaled_x = x // 2
        scaled_y = y // 2
        pg.moveTo(scaled_x, scaled_y)
    elif os_name == 'Windows':
        pg.moveTo(x, y)
#Add error message if not on mac or windows

def performInitial():
    possible_titles = [
        "BlueStacks App Player", "BlueStacks", "BlueStacks X",
        "MuMu Player", "MuMu模拟器","MuMu","网易MuMu模拟器",
        "LDPlayer","LDPlayer9","LDPlayer4","雷电模拟器",
        "Screen Mirroring", "AirPlay"   
    ]
    all_windows = gw.getAllWindows()
    for win in all_windows:
        for title in possible_titles:
            if title.lower() in win.title.lower():
                print(win)
                win.activate()
                return
    print("No valid window found")

def is_green(pixel, tolerance = 60):
    r, g, b = pixel[:3]
    target = (122,206,16)
    return(
        abs(r - target[0]) < tolerance and
        abs(g - target[1]) < tolerance and
        abs(b - target[2]) < tolerance
    )

def is_black(pixel):
    r, g, b = pixel[:3]
    return (r,g,b) == (0,0,0)

def left_anchor(screenshot, start_x, start_y, max_distance = 1000):
    x,y = start_x,start_y

    for _ in range(max_distance):
        x -= 1
        pixel = screenshot.getpixel((x, y))
        if not is_black(pixel):
            continue
        above = screenshot.getpixel((x,y-2))
        below = screenshot.getpixel((x,y+2))
        if is_black(above) and is_black(below):
            return (x,y)

        elif not is_black(below):
            y += 1

        elif not is_black(above):
            y -= 1
    print("No edge found")
    return (x,y)
#I want to add custom error message here

def right_anchor(screenshot, start_x, start_y, max_distance = 1000):
    x,y = start_x,start_y

    for _ in range(max_distance):
        x += 1
        pixel = screenshot.getpixel((x, y))
        black_count = 0

        for i in range(10):
            ny = y + i
            pixel = screenshot.getpixel((x, ny))
            if is_black(pixel):
                black_count += 1
            else:
                break

        if black_count == 10:
            return (x,y)
    print("No edge found")
    return(x,y)

def top_anchor(screenshot, start_x, start_y, max_distance = 1000):
    x,y = start_x,start_y
    for _ in range(max_distance):
        y -= 1
        pixel = screenshot.getpixel((x, y))
        if is_black(pixel):
            return(x,y+1)
    print("No edge found")
    return(x,y)

def bottom_anchor(screenshot, start_x, start_y, max_distance = 1000):
    x,y = start_x,start_y
    for _ in range(max_distance):
        y += 1
        pixel = screenshot.getpixel((x, y))
        if is_black(pixel):
            return(x,y)
    print("No edge found")
    return(x,y)


def grid_check():
    screenshot = pyautogui.screenshot()
    width, height = screenshot.size
    found = False
    cols, rows = 80, 60
    cell_width = int(width // cols)
    cell_height = int(height // rows)

    for gy in range(rows):
        for gx in range(cols):
            center_x = gx * cell_width + cell_width // 2
            center_y = gy * cell_height + cell_height // 2
            if center_x >= width or center_y >= height:
                continue

            pixel = screenshot.getpixel((center_x, center_y))
            if is_green(pixel):
                num_green = 0
                for y in range(rows):
                    for offset in range(-16, 15):
                        if offset == 0:
                            continue
                        ny = gy + offset
                        if 0 <= ny < rows:
                            ny_center = ny * cell_height + cell_height // 2
                            test_pixel = screenshot.getpixel((center_x, ny_center))
                            if is_green(test_pixel):
                                num_green += 1

                        if num_green >= 3:
                            left = left_anchor(screenshot, center_x, center_y)
                            right = right_anchor(screenshot, left[0], left[1])
                            middle_h_1 = (left[0] + right[0]) // 2
                            top = top_anchor(screenshot, middle_h_1, left[1])
                            bottom = bottom_anchor(screenshot, middle_h_1, right[1])
                            height = bottom[1] - top[1]
                            middle_v_1 = (bottom[1] + top[1]) // 2
                            top_1 = top[1]
                            bottom_1 = bottom[1]
                            spacing = height *1.44
                            for i in range(4):
                                offset_y = int(i * spacing)
                                t = int(top[1] + offset_y)
                                b = int(t + height)
                            return (top_1,middle_h_1,middle_v_1, bottom_1,left[0], right[0])
    if not found:
        print("No reset button found")


def firstofday():
    coord_list = grid_check()
    height = coord_list[3] - coord_list[0]
    spacing_v = height*1.44
    offset_y = int(3 * spacing_v)
    t = int(coord_list[0] + offset_y)
    b = int(t + height)
    horizonal = coord_list[5] - coord_list[4]
    reroll_spot = reroll_find()
    move_mouse(reroll_spot[0], reroll_spot[1])
    pg.click()
    time.sleep(.5)
    move_mouse(coord_list[1] - (horizonal * 1.98), b)
    pg.click()
    move_mouse(coord_list[1] - (horizonal * 1.98), b-(height*1.5))
    pg.click()
    move_mouse(reroll_spot[0], reroll_spot[1])

def threeofsame():
    coord_list = grid_check()
    height = coord_list[3] - coord_list[0]
    spacing_v = height*1.44
    offset_y = int(3 * spacing_v)
    t = int(coord_list[0] + offset_y)
    b = int(t + height)
    horizonal = coord_list[5] - coord_list[4]
    reroll_spot = reroll_find()
    move_mouse(reroll_spot[0], reroll_spot[1])
    pg.click()
    time.sleep(.5)
    move_mouse(coord_list[1] - (horizonal * 1.98), b)
    pg.click()
    move_mouse(coord_list[1] - (horizonal * 1.98), b-(height*1.5))
    pg.click()
    move_mouse(reroll_spot[0], reroll_spot[1])
    
def reroll_find():
    coord_list = grid_check()
    height = coord_list[3] - coord_list[0]
    spacing_v = height*1.44
    offset_y = int(3 * spacing_v)
    t = int(coord_list[0] + offset_y)
    b = int(t + height)
    horizonal = coord_list[5] - coord_list[4]
    #move_mouse(coord_list[1] - (horizonal * 2), b+(height*1.5))
    return (coord_list[1] - (horizonal * 2), b+(height*1.5))

def reroll():
    pg.click()
