import django_setup
import logging
import asyncio
import os
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from aiogram_bot.handlers import start, rules, back, contract, contacts, review, questions, no_handlers

load_dotenv()
TOKEN = os.getenv("TOKEN")

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()


async def main():
    """Запуск процесса поллинга новых апдейтов"""
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, skip_updates=True)

if __name__ == "__main__":
    dp.include_routers(start.router)
    dp.include_routers(rules.router)
    dp.include_routers(back.router)
    dp.include_routers(contract.router)
    dp.include_routers(questions.router)
    dp.include_routers(contacts.router)
    dp.include_routers(review.router)
    dp.include_routers(no_handlers.router)

    asyncio.run(main())
