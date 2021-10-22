import os
import tweepy


def get():
    with open(os.path.join(os.path.dirname(__file__), "template.html")) as f:
        return f.read()


def post(screen_name=""):
    CK = os.getenv("TW_CK")
    CS = os.getenv("TW_CS")
    AT = os.getenv("TW_AT")
    AS = os.getenv("TW_AS")
    auth = tweepy.OAuthHandler(CK, CS)
    auth.set_access_token(AT, AS)
    try:
        api = tweepy.API(auth)
        user = api.get_user(screen_name)
        output = "ID: {}".format(user.id)
    except Exception as e:
        print(e)
        if screen_name == "":
            output = ""
        else:
            output = "何かがおかしい。<br>" + str(e)
    return {"output": output}


if __name__ == "__main__":
    print(post("laddge"))
