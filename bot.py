import os
from dotenv import load_dotenv
from aiogram import Bot
from aiogram import Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
import asyncio
from handlers import router

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("Не найден BOT_TOKEN в файле .env")

bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()
dp.include_router(router)


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
