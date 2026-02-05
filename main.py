import asyncio
from os import getenv
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from handlers import router
import handlers
from database import init_db

load_dotenv()
TOKEN = getenv("BOT_TOKEN")


async def main():
    init_db()

    bot = Bot(token=TOKEN)
    handlers.bot = bot

    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)

    print("Start..")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
