import os
import json

image_folder = 'images'
gt_folder = 'groundtruth'
image_extensions = ['.jpg', '.png', '.jpeg']
label_lines = []

for fname in os.listdir(image_folder):
    name, ext = os.path.splitext(fname)
    if ext.lower() in image_extensions:
        gt_file = os.path.join(gt_folder, f"{name}.gt.txt")
        if os.path.exists(gt_file):
            with open(gt_file, 'r', encoding='utf-8') as gt:
                transcription = gt.read().strip()
                label_lines.append(f"{image_folder}/{fname}\t{json.dumps( transcription)}")


with open('label.txt', 'w', encoding='utf-8') as out:
    out.write('\n'.join(label_lines))

