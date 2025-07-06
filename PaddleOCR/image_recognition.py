import os
import yaml
import paddle
import numpy as np
from PIL import ImageGrab
from ppocr.modeling.architectures import build_model
from ppocr.utils.save_load import load_pretrained_params
from ppocr.postprocess import build_post_process

# --- Load Config ---
base_dir = os.path.dirname(__file__)
config_path = os.path.join(base_dir, "configs", "rec", "rec_gameui.yml")

with open(config_path, "r") as f:
    config = yaml.safe_load(f)

# --- Load character dictionary and calculate num_classes ---
dict_path = config["PostProcess"]["character_dict_path"]
with open(dict_path, "r", encoding="utf-8") as f:
    characters = [line.strip() for line in f if line.strip()]
num_classes = len(characters)
if config["PostProcess"].get("use_space_char", False):
    num_classes += 1
config["Architecture"]["Head"]["out_channels"] = num_classes

# --- Build and load model ---
model = build_model(config["Architecture"])
load_pretrained_params(model, config["Global"]["pretrained_model"])
model.eval()

# --- Post-processing ---
postprocess = build_post_process(config["PostProcess"], config["Global"])


import re

def trueOCR(area):
    s_keys = ["def", "debuffresist", "amplifybuff", "dmgresistbypass", "atksp", "hp", "critresist",
              "atk", "dmgresist", "cooldow"]
    s_labels = ["Def", "Debuff Resist", "Amplify Buff", "Dmg Resist Bypass", "Atkspd", "Hp", "Crit Resist",
                "Atk", "Dmg Resist", "Cooldown"]

    # Screenshot and preprocess
    screenshot = ImageGrab.grab(bbox=area).convert("RGB")
    resized_img = screenshot.resize((320, 32))
    image_np = np.array(resized_img).astype("float32") / 255.0
    image_np = (image_np - 0.5) / 0.5
    image_np = image_np.transpose(2, 0, 1)
    image_np = np.expand_dims(image_np, axis=0)

    input_tensor = paddle.to_tensor(image_np)

    with paddle.no_grad():
        pred = model(input_tensor)
        result = postprocess(pred)

    if isinstance(result, list) and len(result) > 0 and isinstance(result[0], (tuple, list)):
        raw_text, score = result[0]
        raw_text_clean = raw_text.lower().replace(",", "").replace(" ", "")

        # Extract percentage if present
        percent_match = re.search(r"\d{1,2}\.?\d{0,2}%", raw_text)
        percent = percent_match.group() if percent_match else None

        for key, label in zip(s_keys, s_labels):
            if key in raw_text_clean:
                if percent:
                    print(f"→ {label}, {percent} (conf: {score:.2f})")
                else:
                    print(f"→ {label} (conf: {score:.2f})")
                return

        # Fallback raw output
        if percent:
            print(f"→ Raw: {raw_text} ({percent}) (conf: {score:.2f})")
        else:
            print(f"→ Raw: {raw_text} (conf: {score:.2f})")
    else:
        print("→ No result")
