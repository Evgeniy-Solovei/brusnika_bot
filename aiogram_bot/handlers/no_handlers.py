from aiogram import Router, types
from aiogram_bot.keyboard.start_keyboard import get_main_keyboard

router = Router()


@router.message()
async def handle_unknown(message: types.Message):
    await message.answer("Выберите действие из меню ниже:", reply_markup=await get_main_keyboard())
