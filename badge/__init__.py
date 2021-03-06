import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont
import os
from io import BytesIO


def get(params, widths):
    params = params.split(",")
    font = PIL.ImageFont.truetype(
        os.path.join(os.path.dirname(__file__), "font.ttf"), 48
    )
    colors = {
        "black": (0, 0, 0),
        "white": (255, 255, 255),
        "red": (255, 0, 0),
        "green": (0, 255, 0),
        "blue": (0, 0, 255),
        "yellow": (255, 255, 0),
        "cyan": (0, 255, 255),
        "magenta": (255, 0, 255),
    }
    img = PIL.Image.new("RGB", (0, 0))
    i = 0
    while i < len(params):
        if params[i + 1] in colors.keys():
            bg = colors[params[i + 1]]
        else:
            params[i + 1] = params[i + 1].strip("#")
            r = int(params[i + 1][0:2], 16)
            g = int(params[i + 1][2:4], 16)
            b = int(params[i + 1][4:6], 16)
            bg = (r, g, b)
        fg = tuple([int(sum(bg) / 3 / 128 + 1) % 2 * 255] * 3)
        text = params[i]
        if i % 4 == 0:
            width = int(widths.split(",")[0])
            if len(widths.split(",")) > 0:
                rwidth = int(widths.split(",")[1])
            else:
                rwidth = int(widths)
            new_img = PIL.Image.new("RGB", (width + rwidth, img.height + 100))
            new_img.paste(img)
            img = new_img
        else:
            if len(widths.split(",")) > 0:
                width = int(widths.split(",")[1])
            else:
                width = int(widths)
        col = PIL.Image.new("RGB", (width, 100), bg)
        draw = PIL.ImageDraw.Draw(col)
        draw.text((int(width / 2), 50), text, fill=fg, font=font, anchor="mm")
        img.paste(col, (int(i % 4 / 2) * (img.width - width), img.height - 100))
        i += 2
    buff = BytesIO()
    img.save(buff, "png")
    return buff.getvalue()
