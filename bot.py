# bot.py

import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

import config
from handlers import common, plan_handler, test_handler 

async def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")
    
    if not config.GEMINI_API_KEY:
        logging.critical("GEMINI_API_KEY не найден! Бот не может запуститься.")
        return
    if not config.BOT_TOKEN:
        logging.critical("BOT_TOKEN не найден! Бот не может запуститься.")
        return

    bot = Bot(token=config.BOT_TOKEN)
    storage = MemoryStorage() 
    dp = Dispatcher(storage=storage)

    dp.include_router(common.router)
    dp.include_router(plan_handler.router)
    dp.include_router(test_handler.router)

    print("Бот (на Gemini) запускается...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен.")