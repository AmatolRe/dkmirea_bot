import hashlib
from random import choice
from PIL import Image, ImageDraw
import numpy as np
import string


def generate(size: int = 120, nick: str = None, color: str = None, background: str = '#f2f1f2') -> Image:
    if not nick:
        nick = ''.join(
            [choice(string.ascii_lowercase + string.digits if i != 5 else string.ascii_uppercase) for i in
             range(6)])

    _bytes = hashlib.md5(nick.encode('utf-8')).digest()

    if not color:
        color = tuple(channel // 2 + 128 for channel in _bytes[6:9])

    _pattern = np.array(
        [bit == '1' for byte in _bytes[3:3 + 9] for bit in bin(byte)[2:].zfill(8)]
    ).reshape(6, 12)
    # Increasing to 12x12 array
    _pattern = np.concatenate((_pattern, _pattern[::-1]), axis=0)

    # Removing blocks at the edges
    for i in range(12):
        _pattern[0, i] = 0
        _pattern[11, i] = 0
        _pattern[i, 0] = 0
        _pattern[i, 11] = 0

    img_size = (size, size)
    block_size = size // 12

    img = Image.new('RGB', img_size, background)
    draw = ImageDraw.Draw(img)

    for x in range(size):
        for y in range(size):
            need_to_paint = _pattern[x // block_size, y // block_size]
            if need_to_paint:
                draw.point((x, y), color)

    return img
