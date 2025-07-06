
from core import *
import os
import sys

# Add PaddleOCR/ to sys.path so imports inside it work
paddleocr_path = os.path.join(os.path.dirname(__file__), "PaddleOCR")
sys.path.append(paddleocr_path)
from image_recognition import trueOCR
regions = find_area()
SCREENSHOT_AREA1, SCREENSHOT_AREA2, SCREENSHOT_AREA3, SCREENSHOT_AREA4 = regions

counter = 0
'''for i in range(1):
    time.sleep(1.5)
    trueOCR(SCREENSHOT_AREA1)
    trueOCR(SCREENSHOT_AREA2)
    trueOCR(SCREENSHOT_AREA3)
    trueOCR(SCREENSHOT_AREA4)
    time.sleep(0.5)
    counter += 1'''

