import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont
import re
import os
from io import BytesIO


def get(text, bgcolor='(255, 255, 255)', linecolor='(0, 0, 0)'):
    if not bgcolor:
        bgcolor = '(255, 255, 255)'
    if not linecolor:
        linecolor = '(0, 0, 0)'
    bgcolor = tuple([int(s.strip('()')) for s in bgcolor.split(',')])
    linecolor = tuple([int(s.strip('()')) for s in linecolor.split(',')])
    tl = text.strip().split('\n')
    dummy = PIL.ImageDraw.Draw(PIL.Image.new('RGB', (0, 0)))
    font = PIL.ImageFont.truetype(
        os.path.join(os.path.dirname(__file__), 'font.ttf'), 36
    )
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
                if w <= 540:
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
        ih = 360
    else:
        ih = h + 120
    img = PIL.Image.new('RGB', (640, ih), bgcolor)
    draw = PIL.ImageDraw.Draw(img)
    draw.text(((640 - w) / 2, (ih - h - 60) / 2), text, fill=(30, 30, 30), font=font)
    r = 20
    lw = 5
    m = 7
    lm = m + lw / 2
    draw.line((lm, lm + r - 1, lm, ih - lm - r + 1), fill=linecolor, width=lw)
    draw.line((lm + r - 1, lm, 640 - lm - r + 1, lm), fill=linecolor, width=lw)
    draw.line((640 - lm, lm + r - 1, 640 - lm, ih - lm - r + 1), fill=linecolor, width=lw)
    draw.line((lm + r - 1, ih - lm, 640 - lm - r + 1, ih - lm), fill=linecolor, width=lw)
    draw.arc((m, m, m + r * 2, m + r * 2), start=180, end=270, fill=linecolor, width=lw)
    draw.arc(
        (640 - m - r * 2 - 1, m, 640 - m - 1, m + r * 2),
        start=270,
        end=360,
        fill=linecolor,
        width=lw,
    )
    draw.arc(
        (640 - m - r * 2 - 1, ih - m - r * 2 - 1, 640 - m - 1, ih - m - 1),
        start=0,
        end=90,
        fill=linecolor,
        width=lw,
    )
    draw.arc(
        (m, ih - m - r * 2 - 1, m + r * 2, ih - m - 1),
        start=90,
        end=180,
        fill=linecolor,
        width=lw,
    )
    logo_base = PIL.Image.new('RGBA', img.size, (255, 255, 255, 0))
    logo = PIL.Image.open(os.path.join(os.path.dirname(__file__), 'logo.png')).resize(
        (60, 60)
    )
    logo_base.paste(logo, (290, ih - 90))
    img = PIL.Image.alpha_composite(img.convert('RGBA'), logo_base.convert('RGBA'))
    buff = BytesIO()
    img.save(buff, 'png')
    return buff.getvalue()


if __name__ == '__main__':
    get(
        '''hello, world
こんにちは😃'''
    )
