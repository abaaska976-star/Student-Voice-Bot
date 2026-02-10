import asyncio
from os import getenv
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

import handlers
from database import init_db

load_dotenv()
TOKEN = getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("BOT_TOKEN не найден в .env!")

async def main():
    init_db()  # Инициализация базы данных

    bot = Bot(token=TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    # Передаём bot в handlers
    handlers.bot = bot
    dp.include_router(handlers.router)

    print("Бот запускается..")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
