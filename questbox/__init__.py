from jinja2 import Environment, FileSystemLoader
import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont
import re
import time
import os
from linebot import LineBotApi
from linebot.models import ImageSendMessage


def get(id):
    env = Environment(loader=FileSystemLoader(os.path.dirname(__file__), encoding='utf8'))
    html = env.get_template('get.html').render({'id': id})
    return html


def post(id, lineid, text):
    tl = text.strip().split('\n')
    dummy = PIL.ImageDraw.Draw(PIL.Image.new('RGB', (0, 0)))
    font = PIL.ImageFont.truetype(os.path.join(os.path.dirname(__file__), 'font.ttf'), 36)
    i = 0
    while True:
        if i + 1 > len(tl):
            break
        line = tl[i].strip()
        if len(line) != 0:
            for rem in range(len(line)):
                if rem == 0:
                    instext = line
                else:
                    instext = line[:-rem]
                w, h = dummy.textsize(instext, font=font)
                if w <= 560:
                    break
            remlen = len(line) - len(instext)
            if remlen != 0:
                tl[i] = line[:-remlen]
                tl.insert(i + 1, line[-remlen:])
        i += 1
    text = '\n'.join(tl)
    text = re.sub('\n\n\n+', '\n\n', text)
    w, h = dummy.textsize(text, font=font)
    if h <= 240:
        ih = 300
    else:
        ih = h + 120
    img = PIL.Image.new('RGB', (660, ih), (244, 245, 257))
    draw = PIL.ImageDraw.Draw(img)
    draw.text(((660 - w) / 2, (ih - h - 60) / 2), text, fill=(30, 30, 30), font=font)
    r = 20
    lw = 5
    m = 7
    lm = m + lw / 2
    color = (40, 163, 204)
    draw.line((lm, lm + r - 1, lm, ih - lm - r + 1), fill=color, width=lw)
    draw.line((lm + r - 1, lm, 660 - lm - r + 1, lm), fill=color, width=lw)
    draw.line((660 - lm, lm + r - 1, 660 - lm, ih - lm - r + 1), fill=color, width=lw)
    draw.line((lm + r - 1, ih - lm, 660 - lm - r + 1, ih - lm), fill=color, width=lw)
    draw.arc((m, m, m + r * 2, m + r * 2), start=180, end=270, fill=color, width=lw)
    draw.arc((660 - m - r * 2 - 1, m, 660 - m - 1, m + r * 2),
             start=270, end=360, fill=color, width=lw)
    draw.arc((660 - m - r * 2 - 1, ih - m - r * 2 - 1, 660 - m -
             1, ih - m - 1), start=0, end=90, fill=color, width=lw)
    draw.arc((m, ih - m - r * 2 - 1, m + r * 2, ih - m - 1),
             start=90, end=180, fill=color, width=lw)
    logo_base = PIL.Image.new('RGBA', img.size, (255, 255, 255, 0))
    logo = PIL.Image.open(os.path.join(os.path.dirname(__file__), 'logo.png')).resize((60, 60))
    logo_base.paste(logo, (325, ih - 90))
    img = PIL.Image.alpha_composite(img.convert('RGBA'), logo_base.convert('RGBA'))
    path = 'img/{}.png'.format(time.time())
    img.save(os.path.join(os.path.dirname(__file__), path))
    url = 'https://{}/questbox/{}'.format(os.getenv('DOMAIN'), path)
    line_bot_api = LineBotApi(os.getenv('LINE_AT'))
    line_bot_api.push_message(lineid, ImageSendMessage(
        original_content_url=url, preview_image_url=url
    ))
    env = Environment(loader=FileSystemLoader(os.path.dirname(__file__), encoding='utf8'))
    html = env.get_template('post.html').render({'id': id, 'url': url})
    return html


if __name__ == '__main__':
    post('''hello, world
こんにちは😃''')
