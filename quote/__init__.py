from PIL import Image
from .generator import get


def generate(quote: str,
             title: str = 'Цитаты БСБО-07-20',
             disable_title: bool = False,
             color: str = 'white',
             anon: bool = False,
             avatar: Image = None,
             author_name: str = 'Какой-то человек',
             back: Image = None,
             blur: int = 2,
             ) -> Image:
    """
    Quote generator
    :param quote: str,
    :param title: str,
    :param disable_title: bool,  # False
    :param color: str,  # white
    :param anon: bool,  # False
    :param avatar: Image,  # None
    :param author_name: str,  # Base Name
    :param back: Image,  # None
    :param blur: int,  # 2
    :return: Image (Pillow obj)
    """
    if not quote:
        raise Exception('The quote should not be empty')
    return get(quote, title, disable_title, color, anon, avatar, author_name, back, blur)
