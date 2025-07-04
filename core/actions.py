import cv2
import numpy as np
import pyautogui
import pyautogui as pg
from pathlib import Path
import pytesseract
from PIL import ImageGrab, ImageDraw
import time
import platform
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
    pg.keyDown('command')
    pg.press('tab')
    pg.keyUp('command')
#Fix this shit bro


def reroll():
    # To do: Localize this for everyone
    pg.moveTo(795, 453)
    pg.click()

def is_green(pixel, tolerance = 60):
    r, g, b = pixel[:3]
    target = (122,206,16)
    return(
        abs(r - target[0]) < tolerance and
        abs(g - target[1]) < tolerance and
        abs(b - target[2]) < tolerance
    )

def grid_check():
    screenshot = pyautogui.screenshot()
    width, height = screenshot.size
    draw = ImageDraw.Draw(screenshot)
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
                            top_left = (gx * cell_width, gy * cell_height)
                            bottom_right = ((gx + 1) * cell_width, (gy + 1) * cell_height)
                            draw.rectangle([top_left, bottom_right], outline="red", width=3)
                            if
                            print(center_x, center_y)
                            print(screenshot.size)
                            found = True
                            return
    if not found:
        print("No reset button found")


def firstofday():
    base_image = pg.locateOnScreen(str(BASE_DIR / 'reqimage' / 'firstofday.png'), confidence=0.7)
    if base_image:
        screenshot = pyautogui.screenshot()
        crop_box = (
            base_image.left + 30,
            base_image.top + 100,
            base_image.left + 700,
            base_image.top + 570
        )
        region = screenshot.crop(crop_box)
        data = pytesseract.image_to_data(region, output_type=pytesseract.Output.DICT)
        text = pytesseract.image_to_string(region, lang='eng')
        print(data)
        for i, text in enumerate(data['text']):
            if data['text'][i] == "today":
                y = (data['top'][i + 1] + crop_box[1] // 2) - 190
                x = (data['left'][i + 1] + crop_box[0] // 2) - 200
                pg.moveTo(x, y)
                pg.click()
                break


performInitial()
grid_check()

