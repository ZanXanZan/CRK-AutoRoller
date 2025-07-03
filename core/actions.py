import pyautogui
import pyautogui as pg
from pathlib import Path
import pytesseract
from PIL import ImageGrab, ImageDraw
import time
BASE_DIR = Path(__file__).resolve().parent.parent
def performInitial():

    pg.keyDown('command')
    pg.press('tab')
    pg.keyUp('command')

def reroll():
    #To do: Localize this for everyone
    pg.moveTo(795, 453)
    pg.click()

def firstofday():
    base_image = pg.locateOnScreen(str(BASE_DIR / 'reqimage'/ 'firstofday.png'),confidence=0.7)
    if base_image:
        screenshot = pyautogui.screenshot()
        crop_box = (
            base_image.left+30,
            base_image.top+100,
            base_image.left+700,
            base_image.top+570
        )
        region = screenshot.crop(crop_box)
        data = pytesseract.image_to_data(region, output_type=pytesseract.Output.DICT)
        text = pytesseract.image_to_string(region, lang='eng')
        print(data)
        for i, text in enumerate(data['text']):
            if data['text'][i] == "today":
                y = (data['top'][i+1]+crop_box[1]//2)-190
                x = (data['left'][i+1]+crop_box[0]//2)-200
                pg.moveTo(x,y)
                pg.click()
                break



    #We still need to click ok after this by the way this is only half the code