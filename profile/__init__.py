import os
import time
import json
import base64
import requests
import tweepy


def get():
    if os.path.isfile("./profile_cache.json"):
        with open("./profile_cache.json") as f:
            d = json.load(f)
        updated = d.get("updated") if d.get("updated") else 0
        if updated > time.time() - 900:
            return d
    CK = os.getenv("TW_CK")
    CS = os.getenv("TW_CS")
    AT = os.getenv("TW_AT")
    AS = os.getenv("TW_AS")
    auth = tweepy.OAuthHandler(CK, CS)
    auth.set_access_token(AT, AS)
    api = tweepy.API(auth)
    user = api.get_user(user_id=1253674340228292608)
    d = {}
    d["name"] = user.name
    d["screen_name"] = user.screen_name
    d["follower"] = user.followers_count
    d["follow"] = user.friends_count
    d["desc"] = user.description
    r0 = requests.get(user.profile_banner_url)
    d["profile_banner"] = (
        "data:"
        + r0.headers["Content-Type"]
        + ";"
        + "base64,"
        + base64.b64encode(r0.content).decode()
    )
    r1 = requests.get(user.profile_image_url_https)
    d["profile_image"] = (
        "data:"
        + r1.headers["Content-Type"]
        + ";"
        + "base64,"
        + base64.b64encode(r1.content).decode()
    )
    d["updated"] = time.time()
    with open("./profile_cache.json", "w") as f:
        json.dump(d, f)
    return d
