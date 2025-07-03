import os
import yaml
import paddle
import numpy as np
from PIL import ImageGrab

from ppocr.modeling.architectures import build_model
from ppocr.utils.save_load import load_pretrained_params
from ppocr.postprocess import build_post_process
from ppocr.data.imaug import create_operators

# Constants
# --- Load Config ---
base_dir = os.path.dirname(__file__)
config_path = os.path.join(base_dir, "configs", "rec", "rec_gameui.yml")

with open(config_path, "r") as f:
    config = yaml.safe_load(f)

# --- Build Model ---
model = build_model(config["Architecture"])
load_pretrained_params(model, config["Global"]["pretrained_model"])
model.eval()

# --- Post-processing ---
postprocess = build_post_process(config["PostProcess"], config["Global"])

# --- Build Cleaned-Up Operators (no DecodeImage or label transforms) ---
ops = create_operators(config["Eval"]["dataset"]["transforms"], config["Global"])
ops = [op for op in ops if op.__class__.__name__ not in ["DecodeImage", "RecLabelEncode", "CTCLabelEncode", "KeepKeys"]]

# --- OCR Function ---
def trueOCR(area):
    s = ["def", "debuffresist", "amplifybuff", "dmgresistbypass", "atksp", "hp", "critresist",
         "atk","dmgresist" ,"cooldow"]
    y = ["Def", "Debuff Resist", "Amplify Buff", "Dmg Resist Bypass", "Atkspd", "Hp", "Crit Resist",
         "Atk","Dmg Resist" ,"Cooldown"]
    screenshot = ImageGrab.grab(bbox=area).convert("RGB")
    image_np = np.array(screenshot)
    image_bgr = image_np[..., ::-1]

    data = {"image": image_bgr}

    for op in ops:
        data = op(data)

    if isinstance(data, list):
        data = data[0]


    input_tensor = paddle.to_tensor(np.expand_dims(data["image"], axis=0))

    with paddle.no_grad():
        pred = model(input_tensor)
        result = postprocess(pred)

    if isinstance(result, list) and len(result) > 0 and isinstance(result[0], (tuple, list)):
        text, score = result[0]
        for i, stat in enumerate(s):
            if stat not in text:
                continue

            index = text.find(stat)
            remaining = text[index + len(stat):]
            number = ''
            for char in remaining:
                if char.isdigit():
                    number += char
                else:
                    break

            if not number:
                print(text)
                continue

            stat = y[i]
            decimal_number = float(number)
            if len(number) == 2 and stat != "Hp" and stat != "Dmg Resist Bypass":
                insert = '.'
                numberstring = str(number)
                mid = len(numberstring) // 2
                newNumber = numberstring[:mid] + insert + numberstring[mid:]
                decimal_number = float(newNumber)

            if len(number) == 3:
                decimal_str = number[:-1] + '.' + number[-1:]
                decimal_number = float(decimal_number)

            print(stat + "    " + str(decimal_number))


