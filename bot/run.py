import asyncio
import os
from aiogram import Dispatcher, Bot
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ.get('TOKEN') or ''

bot = Bot(token=TOKEN)

dp = Dispatcher()
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    
    asyncio.run(main())


