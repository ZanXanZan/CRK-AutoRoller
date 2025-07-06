
from core import *
import os
import sys

# Add PaddleOCR/ to sys.path so imports inside it work
paddleocr_path = os.path.join(os.path.dirname(__file__), "PaddleOCR")
sys.path.append(paddleocr_path)
from image_recognition import trueOCR
SCREENSHOT_AREA1 = (570, 262, 900, 290)  # Left, top, right, down
SCREENSHOT_AREA2 = (570, 302, 900, 330)
SCREENSHOT_AREA3 = (570, 342, 900, 370)
SCREENSHOT_AREA4 = (570, 381, 900, 410)
performInitial()
counter = 0
for i in range(3):
    reroll()
    time.sleep(1.5)
    trueOCR(SCREENSHOT_AREA1)
    trueOCR(SCREENSHOT_AREA2)
    trueOCR(SCREENSHOT_AREA3)
    trueOCR(SCREENSHOT_AREA4)
    time.sleep(0.5)
    counter += 1

