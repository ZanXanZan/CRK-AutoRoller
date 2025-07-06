
from core import *
import os
import sys

# Add PaddleOCR/ to sys.path so imports inside it work
paddleocr_path = os.path.join(os.path.dirname(__file__), "PaddleOCR")
sys.path.append(paddleocr_path)
from image_recognition import trueOCR
performInitial()
time.sleep(1)
regions = find_area()
SCREENSHOT_AREA1, SCREENSHOT_AREA2, SCREENSHOT_AREA3, SCREENSHOT_AREA4 = regions
time.sleep(2)
for i in range(5):
    if i == 0:
        firstofday()
    time.sleep(3)
    reroll()
    time.sleep(2)
    trueOCR(SCREENSHOT_AREA1)
    trueOCR(SCREENSHOT_AREA2)
    trueOCR(SCREENSHOT_AREA3)
    trueOCR(SCREENSHOT_AREA4)

