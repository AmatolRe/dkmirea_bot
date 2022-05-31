from io import BytesIO

from PIL import Image, ImageDraw, ImageFont

import quote.rnd_avatar as ava
import requests
import textwrap

header_font = ImageFont.truetype("quote/Roboto-Emoji-Regular.ttf", 45)
quote_font = ImageFont.truetype("quote/Roboto-Emoji-Regular.ttf", 35)
author_font = ImageFont.truetype("quote/Roboto-Emoji-Regular.ttf", 30)


# https://ru.stackoverflow.com/questions/581788/Как-создать-круглый-портрет-в-pil
def round_mask(size, antialias: int = 2) -> Image:
    """
    Круглая маска для аватара
    :param size: размер изображения
    :param antialias: сглаживание
    :return:
    """
    mask = Image.new("L", (size[0] * antialias, size[1] * antialias), 0)
    ImageDraw.Draw(mask).ellipse((0, 0) + mask.size, fill=255)
    return mask.resize(size, Image.ANTIALIAS)


def crop(im, s) -> Image:
    """
    Обрезка изображения
    :param im:
    :param s:
    :return:
    """
    w, h = im.size
    k = w / s[0] - h / s[1]
    if k > 0:
        im = im.crop(((w - h) / 2, 0, (w + h) / 2, h))
    elif k < 0:
        im = im.crop((0, (h - w) / 2, w, (h + w) / 2))
    return im.resize(s, Image.ANTIALIAS)


def prepare_text(quote: str):
    """
    Проверка и подготовка текста
    :param quote:
    :return:
    """
    quote = quote.replace('  ', ' ')
    if len(quote) > 1240:
        raise Exception('Text is too long')

    wrapped_quote = []

    for q_part in quote.split('\n'):
        for q in textwrap.wrap(q_part, 39, replace_whitespace=False):
            wrapped_quote.append(q)

    if len(wrapped_quote) > 150:
        raise Exception('Text is too long')

    quote = '«' + '\n'.join(wrapped_quote) + '»'
    wrap = 43
    text_height = 0

    for qq in wrapped_quote:
        current_wrap = wrap
        lines = qq.count('\n')
        if lines > 0:
            lines = lines + 1
            current_wrap = current_wrap * lines
        text_height = text_height + current_wrap + 1

    return quote, text_height


def make_image(
        text_color: str,

        quote: str,
        title: str,
        disable_title: bool,

        anon: bool,
        avatar: Image,
        author_name: str,

        text_height: int,
        back: Image,
        blur: int,

) -> Image:
    if anon:
        img_height = text_height + 280
    else:
        img_height = text_height + 350
    img = Image.new("RGB", (900, img_height), 'black')

    if back is None:
        res = requests.get(f'https://picsum.photos/900/{img_height}/?blur={blur}')
        back = Image.open(BytesIO(res.content))
        back.putalpha(70)
        img.paste(back, (0, 0), back)
    else:
        raise Exception('Something went wrong...')

    draw = ImageDraw.Draw(img)

    if not disable_title:
        draw.text((100, 50), title, fill=text_color, font=header_font)

    y = 150
    draw.multiline_text((100, y), quote, fill=text_color, font=quote_font, spacing=12)

    if anon:
        pass
    else:
        draw.text(
            (230, img_height - 120),
            "— " + author_name,
            fill=text_color,
            font=author_font,
        )

        if avatar:
            pass
        else:
            avatar = ava.generate(size=120)
            avatar = avatar.resize((100, 100))
            avatar.convert("RGBA")
            avatar = crop(avatar, avatar.size)
            avatar.putalpha(round_mask(avatar.size, 4))
            img.paste(avatar, (100, img_height - 150), avatar)

    return img


def get(
        quote: str,
        title: str,
        disable_title: bool,  # False
        color: str,  # white
        anon: bool,  # False
        avatar: Image,  # None
        author_name: str,  # Base Name
        back: Image,  # None
        blur: int,  # 2
) -> Image:
    quote, height = prepare_text(quote)
    return make_image(color, quote, title, disable_title, anon, avatar, author_name, height, back, blur)