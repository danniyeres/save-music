import asyncio
import logging
from aiogram import Bot, Dispatcher
from bot.config import BOT_TOKEN as TOKEN
from bot.handlers import start, text


async def main():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    dp.include_router(start.router)
    dp.include_router(text.router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())