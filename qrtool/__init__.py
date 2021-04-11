import os
from base64 import b64decode, b64encode
from io import BytesIO

import qrcode
from jinja2 import Environment, FileSystemLoader
from PIL import Image
from pyzbar.pyzbar import decode


def make(string):
    img = qrcode.make(string)
    buf = BytesIO()
    img.save(buf, format='png')
    b64 = b64encode(buf.getvalue()).decode()
    return b64


def read(b64):
    data = b64decode(b64)
    buf = BytesIO(data)
    img = Image.open(buf)
    if decode(img):
        string = decode(img)[0].data.decode()
    else:
        string = ''
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
