import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import Message, ContentType, InputFile, ChatActions

from io import BytesIO
import quote

from config import TOKEN

logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Бот запускается")

    bot = Bot(token=TOKEN)
    dp = Dispatcher(bot)

    async def user_start(message: Message):
        await message.reply("Hello! Send text for quote 📄\nBot by Daniil Kudryashov BSBO-07-20")

    async def generate_quote(message: Message):
        await ChatActions.typing()
        new_msg = await message.reply("Generation started ❇️\nThis may take about a minute")
        image = quote.generate(quote=message.text, author_name=message.from_user.full_name)
        # image.show()
        buff = BytesIO()
        image.save(buff, format="jpeg")
        buff.seek(0)
        photo = InputFile(path_or_bytesio=buff)
        await ChatActions.upload_photo()
        await new_msg.delete()
        await message.answer_photo(photo=photo)

    async def empty_reply(message: Message):
        await message.reply("The bot can process only text 📝")

    dp.register_message_handler(user_start, commands=["start"], state="*")
    dp.register_message_handler(generate_quote, content_types=ContentType.TEXT)
    dp.register_message_handler(empty_reply, content_types=ContentType.ANY)

    # start
    try:
        await dp.start_polling()
    finally:
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Бот остановлен")
