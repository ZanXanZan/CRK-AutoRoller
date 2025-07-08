
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
time.sleep(2)
for i in range(1):
    if i == 0:
        #firstofday()
        time.sleep(2)
    else:
        reroll()
        time.sleep(2)
    
    for region in regions:
        trueOCR(region)
    

