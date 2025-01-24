from aiogram import Router, types
from aiogram.filters import Command
from aiogram_bot.keyboard.start_keyboard import get_main_keyboard
from bot_core.models import UserProfile

router = Router()


@router.message(Command("start"))
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username
    user_profile, created = await UserProfile.objects.aget_or_create(
        user_id=user_id, username=username)
    welcome_text = (
        "Добро пожаловать! 🏨\n"
        "Выберите нужную категорию из меню ниже:")
    keyboard = await get_main_keyboard()
    await message.answer(welcome_text, reply_markup=keyboard)
