from pathlib import Path
from openai import OpenAI
import base64
from PIL import ImageGrab
from core.secretkey import my_sk


# Screenshot area we need to think of a solution for this
# My initial thoughts is that we can look for pixels of the right color, since it should be constant
# We can then use the pixel patterns for area and other such
BASE_DIR = Path(__file__).resolve().parent.parent

client = OpenAI(api_key=my_sk)

def save_image(counter, area):
    screenshot = ImageGrab.grab(bbox=area)
    image_name = counter+".png"
    image_path = f"/Users/grantbiellak/PycharmProjects/CRK-AutoRoller/data/images/{image_name}"
    screenshot.save(image_path)
    return image_path
def encode_image(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def get_gt(counter,area):
    gt_path = BASE_DIR / 'data' / 'groundtruth' / f'{counter}.gt.txt'
    prediction = openai_train(counter,area)

    with open(gt_path, "w") as f:
        f.write(prediction.strip())

def openai_train(counter,area):
    path = save_image(counter,area)
    b64 = encode_image(path)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Respond in exactly 1 line. "
                                             "Each line should be parameter, value, "
                                             "using only the values visible in the image. "
                                             "Do not add explanations."},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{b64}"
                        }
                    }
                ]
            }
        ],
        max_tokens=100
    )

    return response.choices[0].message.content