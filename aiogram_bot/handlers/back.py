from aiogram import Router, types
from aiogram_bot.handlers.start import cmd_start

router = Router()


@router.message(lambda message: message.text == "Назад")
async def handle_back(message: types.Message):
    await cmd_start(message)
