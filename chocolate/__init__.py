import os
from random import randint
from linebot import LineBotApi, WebhookParser
from linebot.models import TextSendMessage


async def post(request):
    line_api = LineBotApi(channel_access_token=os.getenv("CHOCO_LINE_AT"))
    parser = WebhookParser(channel_secret=os.getenv("CHOCO_LINE_CS"))
    events = parser.parse((await request.body()).decode("utf-8"),
                          request.headers.get("X-Line-Signature", ""))
    for ev in events:
        match_text = ["チョコ", "ちょこ", "チョコレート", "ちょこれーと", "バレンタイン", "ばれんたいん", "🍫"]
        tosend = False
        for text in match_text:
            if text in ev.message.text:
                tosend = True
                break
        if tosend:
            emojis = [
                {
                    "index": 0,
                    "productId": "5ac2213e040ab15980c9b447",
                    "emojiId": "058"
                },
                {
                    "index": 0,
                    "productId": "5ac2213e040ab15980c9b447",
                    "emojiId": "059"
                },
                {
                    "index": 0,
                    "productId": "5ac2213e040ab15980c9b447",
                    "emojiId": "178"
                },
                {
                    "index": 0,
                    "productId": "5ac2213e040ab15980c9b447",
                    "emojiId": "178"
                },
                {
                    "index": 0,
                    "productId": "5ac2213e040ab15980c9b447",
                    "emojiId": "178"
                },
                {
                    "index": 0,
                    "productId": "5ac2211e031a6752fb806d61",
                    "emojiId": "201"
                },
                {
                    "index": 0,
                    "productId": "5ac1de17040ab15980c9b438",
                    "emojiId": "059"
                },
                {
                    "index": 0,
                    "productId": "5ac1de17040ab15980c9b438",
                    "emojiId": "061"
                },
                {
                    "index": 0,
                    "productId": "5ac1de17040ab15980c9b438",
                    "emojiId": "061"
                },
                {
                    "index": 0,
                    "productId": "5ac1de17040ab15980c9b438",
                    "emojiId": "061"
                },
                {
                    "index": 0,
                    "productId": "5ac2211e031a6752fb806d61",
                    "emojiId": "182"
                },
                {
                    "index": 0,
                    "productId": "5ac2197b040ab15980c9b43d",
                    "emojiId": "010"
                },
            ]
            line_api.reply_message(
                ev.reply_token,
                TextSendMessage(text="$", emojis=[emojis[randint(0, len(emojis) - 1)]]))
    return "ok"
