import os
import base64
import PIL.Image
from io import BytesIO


def dec2qui(x):
    if int(x / 5):
        return dec2qui(int(x / 5)) + str(x % 5)
    return str(x % 5)


def encode(img, text):
    b64 = base64.b64encode(text.encode()).decode() + "*"
    ucp = [dec2qui(ord(s)) for s in b64]
    img_w, img_h = img.size
    if img_w * img_h < len(b64):
        mpr = int(len(b64) / img_w / img_h) + 1
        img_w, img_h = (img_w * mpr, img_h * mpr)
        img = img.resize((img_w, img_h))
    p = 0
    for x in range(img_w):
        for y in range(img_h):
            if p >= len(ucp):
                break
            pix = list(img.getpixel((x, y)))
            pix[0] = pix[0] // 5 * 5 + int(ucp[p][0])
            pix[1] = pix[1] // 5 * 5 + int(ucp[p][1])
            pix[2] = pix[2] // 5 * 5 + int(ucp[p][2])
            img.putpixel((x, y), tuple(pix))
            p += 1
    return img


def decode(img):
    ucp = []
    done = False
    for x in range(img.width):
        for y in range(img.height):
            if done:
                break
            pix = list(img.getpixel((x, y)))
            ucp.append("{}{}{}".format(pix[0] % 5, pix[1] % 5, pix[2] % 5))
            if ucp[-1] == "132":
                done = True
    b64 = ""
    for u in ucp:
        b64 += chr(int(u, 5))
    return base64.b64decode(b64.encode()).decode()


def post_encode(img_bin, text):
    img = encode(PIL.Image.open(BytesIO(img_bin)), text)
    buff = BytesIO()
    img.save(buff, "png")
    return {"output": base64.b64encode(buff.getvalue()).decode().replace("'", "")}


def post_decode(img_bin):
    text = decode(PIL.Image.open(BytesIO(img_bin)))
    return {"output": text}


def get():
    with open(os.path.join(os.path.dirname(__file__), "get.html")) as f:
        return f.read()
