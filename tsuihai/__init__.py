import os
import datetime
import tweepy
from jinja2 import Environment, FileSystemLoader


def main(user=""):
    CK = os.getenv("TW_CK")
    CS = os.getenv("TW_CS")
    AT = os.getenv("TW_AT")
    AS = os.getenv("TW_AS")
    auth = tweepy.OAuthHandler(CK, CS)
    auth.set_access_token(AT, AS)
    try:
        api = tweepy.API(auth)
        print(type(user))
        getuser = api.get_user(user)
        created = getuser.created_at
        today = datetime.datetime.now()
        passed = today - created
        min = passed.total_seconds() / 3600
        tweets = getuser.statuses_count
        tsuihaido = round(tweets / min * 100 - 100) / 100
        output = (
            user
            + "さんのツイ廃度は <b>"
            + str(tsuihaido)
            + '</b> <a href="https://twitter.com/share" class="twitter-share-button" data-text="'
            + user
            + "さんのツイ廃は "
            + str(tsuihaido)
            + ' です" data-hashtags="ツイ廃度測定">Tweet</a> '
        )
    except Exception as e:
        print(e)
        if user == "":
            output = ""
        else:
            output = "何かがおかしい。<br>" + str(e)
    env = Environment(
        loader=FileSystemLoader(os.path.dirname(__file__), encoding="utf8")
    )
    return env.get_template("template.html").render(user=user, output=output)


if __name__ == "__main__":
    print(main("laddge"))
