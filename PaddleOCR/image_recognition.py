import os
import yaml
import paddle
import numpy as np
from PIL import ImageGrab
from ppocr.modeling.architectures import build_model
from ppocr.utils.save_load import load_pretrained_params
from ppocr.postprocess import build_post_process
import re

# --- Load Config ---
base_dir = os.path.dirname(__file__)
config_path = os.path.join(base_dir, "configs", "rec", "rec_gameui.yml")

with open(config_path, "r") as f:
    config = yaml.safe_load(f)

# --- Load character dictionary and set num_classes ---
dict_path = config["PostProcess"]["character_dict_path"]
with open(dict_path, "r", encoding="utf-8") as f:
    characters = [line.strip() for line in f if line.strip()]
num_classes = len(characters)
if config["PostProcess"].get("use_space_char", False):
    num_classes += 1
config["Architecture"]["Head"]["out_channels"] = num_classes

# --- Build and load model ---
model = build_model(config["Architecture"])

pretrained_path = config["Global"].get("pretrained_model", None)
if pretrained_path:
    load_pretrained_params(model, pretrained_path)
model.eval()

# --- Post-process function ---
postprocess = build_post_process(config["PostProcess"], config["Global"])

# --- OCR Function ---
def trueOCR(area):
    # Label keys for matching common game UI stats
    s_keys = ["def", "debuffresist", "amplifybuff", "dmgresistbypass", "atksp", "hp", "critresist",
              "atk", "dmgresist", "cooldow"]
    s_labels = ["Def", "Debuff Resist", "Amplify Buff", "Dmg Resist Bypass", "Atkspd", "Hp", "Crit Resist",
                "Atk", "Dmg Resist", "Cooldown"]

    # Capture screenshot and resize to training input size (Width x Height)
    screenshot = ImageGrab.grab(bbox=area).convert("RGB")
    resized_img = screenshot.resize((330, 32))  # matches [3, 32, 330]

    # Normalize image: use BGR mean/std from config Train transforms
    # Your config uses BGR with mean/std 127.5 and scale 1/255 in transforms,
    # but the inference pipeline usually normalizes by (img / 255 - mean/127.5)
    # For simplicity, replicate same normalization as training:

    image_np = np.array(resized_img).astype("float32")
    # Convert RGB to BGR (since your train config DecodeImage uses BGR)
    image_np = image_np[:, :, ::-1]

    # Normalize: (img / 255 - 0.5) / 0.5  matches scale=1/255 and mean/std 127.5
    image_np = image_np / 255.0
    image_np = (image_np - 0.5) / 0.5

    # Change to CHW format and add batch dim
    image_np = image_np.transpose(2, 0, 1)
    image_np = np.expand_dims(image_np, axis=0)

    input_tensor = paddle.to_tensor(image_np)

    # Model inference
    with paddle.no_grad():
        preds = model(input_tensor)
        result = postprocess(preds)

    # Process result
    if isinstance(result, list) and len(result) > 0 and isinstance(result[0], (tuple, list)):
        raw_text, score = result[0]
        raw_text_clean = raw_text.lower().replace(",", "").replace(" ", "")
        percent_match = re.search(r"\d{1,2}\.?\d{0,2}%", raw_text)
        percent = percent_match.group() if percent_match else None

        for key, label in zip(s_keys, s_labels):
            if key in raw_text_clean:
                if percent:
                    print(f"→ {label}, {percent} (conf: {score:.2f})")
                else:
                    print(f"→ {label} (conf: {score:.2f})")
                return

        # Fallback print
        if percent:
            print(f"→ Raw: {raw_text} ({percent}) (conf: {score:.2f})")
        else:
            print(f"→ Raw: {raw_text} (conf: {score:.2f})")
    else:
        print("→ No result")
