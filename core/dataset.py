import os
import csv
from datetime import datetime
from PIL import Image

IMAGE_FOLDER = 'data/images'
GROUND_TRUTH_FOLDER = 'data/groundtruth.txt'
CSV_FILE = 'data/dataset.csv'


def save_ground_truth(filename: str, text: str):
    gt_filename = filename.replace('.png', '.gt.txt')
    gt_filepath = os.path.join(IMAGE_FOLDER, gt_filename)
    with open(gt_filepath, 'w') as f:
        f.write(text)

    with open(GROUND_TRUTH_FOLDER, 'a', encoding='utf-8') as f:
        f.write(f'{filename},\t{text}\n')

