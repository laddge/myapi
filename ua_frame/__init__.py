import os
import tweepy
import base64
from io import BytesIO
from PIL import Image, ImageDraw
import requests


def get():
    with open(os.path.join(os.path.dirname(__file__), "template.html")) as f:
        return f.read()


def post(screen_name):
    CK = os.getenv("TW_CK")
    CS = os.getenv("TW_CS")
    AT = os.getenv("TW_AT")
    AS = os.getenv("TW_AS")
    auth = tweepy.OAuthHandler(CK, CS)
    auth.set_access_token(AT, AS)
    status = 0
    resdata = ""
    try:
        api = tweepy.API(auth)
        user = api.get_user(screen_name=screen_name)
        res = requests.get(user.profile_image_url.replace('_normal', ''))
        print(user.profile_image_url.replace('normal', 'bigger'))
        icon = Image.open(BytesIO(res.content))
        size = icon.size[0]
        scaled = int(size * 0.875)
        mask = Image.new("L", icon.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, size, size), fill=255)
        icon = icon.copy()
        icon.putalpha(mask)
        icon = icon.resize(size=(scaled, scaled))
        bg = Image.new("RGB", (size, size), (0, 90, 187))
        bg_d = ImageDraw.Draw(bg)
        bg_d.rectangle((0, size / 2, size, size), fill=(255, 213, 0))
        pos = int((size - scaled) / 2)
        clear = Image.new("RGBA", (size, size), (255, 255, 255, 0))
        clear.paste(icon, (pos, pos))
        bg = Image.alpha_composite(bg, clear)
        buffer = BytesIO()
        bg.save(buffer, format="PNG")
        resdata = base64.b64encode(buffer.getvalue()).decode().replace("'", "")
    except Exception as e:
        print(e)
        status = 1
    return {"status": status, "data": resdata}


if __name__ == "__main__":
    print(get())
