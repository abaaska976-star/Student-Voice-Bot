import asyncio
from os import getenv
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from handlers import router
from database import init_db  # твой asyncpg init_db

load_dotenv()
TOKEN = getenv("BOT_TOKEN")


async def main():
    # ⚡ ВАЖНО: вызываем init_db с await
    await init_db()  # ← таблицы создадутся в Supabase

    bot = Bot(token=TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)

    print("Start..")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
