from aiogram import Router, types
from bot_core.models import Document

router = Router()


@router.message(lambda message: message.text == "Контакты")
async def handle_contacts(message: types.Message):
    contacts_text = (
        "📞 <b>Телефон:</b> +7 936 000 6257\n"
        "📧 <b>Почта:</b> ooo.brusnika@yandex.ru\n"
        "📱 <b>Telegram:</b> +7 936 000 6257\n"
        "💬 <b>WhatsApp:</b> +7 936 000 6257\n"
    )
    back_button = types.KeyboardButton(text="Назад")
    keyboard = types.ReplyKeyboardMarkup(keyboard=[[back_button]], resize_keyboard=True)
    await message.answer(contacts_text, reply_markup=keyboard, parse_mode="HTML")

