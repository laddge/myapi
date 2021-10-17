import os
import tweepy
import base64
from io import BytesIO
from PIL import Image, ImageDraw
import requests


def get():
    with open(os.path.join(os.path.dirname(__file__), "template.html")) as f:
        return f.read()


def post(username):
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
        user = api.get_user(username)
        res = requests.get(user.profile_image_url.replace('_normal', ''))
        icon = Image.open(BytesIO(res.content))
        size = icon.size[0]
        mask = Image.open(os.path.join(os.path.dirname(__file__), "mask.png"))
        mask = mask.resize(size=(size, size))
        icon = Image.alpha_composite(icon.convert('RGBA'), mask.convert('RGBA'))
        buffer = BytesIO()
        icon.save(buffer, format="PNG")
        resdata = base64.b64encode(buffer.getvalue()).decode().replace("'", "")
    except Exception as e:
        print(e)
        status = 1
    return {"status": status, "data": resdata}


if __name__ == "__main__":
    print(get())
