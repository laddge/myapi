import os
from base64 import b64decode, b64encode
from io import BytesIO

import cv2
import numpy as np
import qrcode
from jinja2 import Environment, FileSystemLoader
from PIL import Image


def make(string):
    img = qrcode.make(string)
    buf = BytesIO()
    img.save(buf, format='png')
    b64 = b64encode(buf.getvalue()).decode()
    return b64


def read(b64):
    data = b64decode(b64)
    buf = BytesIO(data)
    pil_img = Image.open(buf)
    img = np.array(pil_img, dtype=np.uint8)
    if img.ndim == 2:
        pass
    elif img.shape[2] == 3:
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    elif img.shape[2] == 4:
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGRA)
    detector = cv2.QRCodeDetector()
    try:
        data, bbox, straight_qrcode = detector.detectAndDecode(img)
    except Exception:
        string = ''
    else:
        string = data
    return string


def main(string='', b64='', dl=False):
    env = Environment(loader=FileSystemLoader(
        os.path.dirname(__file__), encoding='utf8'))
    if dl:
        dl_btn = '<button onclick="dl();">Download</button>'
    else:
        dl_btn = ''
    return env.get_template('template.html').render(string=string, b64=b64, dl_btn=dl_btn)


if __name__ == '__main__':
    print(main())
