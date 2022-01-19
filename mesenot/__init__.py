import datetime
import os

import requests
from bs4 import BeautifulSoup
from linebot import LineBotApi
from linebot.models import TextSendMessage


def send():
    url = os.getenv('MESENOT_URL')
    lineid = os.getenv('MESENOT_LINEID')
    line_bot_api = LineBotApi(os.getenv('LINE_AT'))
    line_bot_api.push_message(
        lineid, TextSendMessage(text='新しいレポートが配信されました\n{}'.format(url))
    )


def main():
    url = os.getenv('MESENOT_URL')
    res = requests.get(url)
    now = datetime.datetime.now()
    print('[{}] Fetched'.format(now.strftime('%Y/%m/%d %H:%M:%S')))
    el = BeautifulSoup(res.text, 'html.parser').find(attrs={'name': 'period'})
    if os.getenv('MESENOT_CACHE'):
        if os.getenv('MESENOT_CACHE') != str(el):
            send()
            now = datetime.datetime.now()
            print('[{}] LINE sent'.format(now.strftime('%Y/%m/%d %H:%M:%S')))
    os.environ['MESENOT_CACHE'] = str(el)


if __name__ == '__main__':
    main()
