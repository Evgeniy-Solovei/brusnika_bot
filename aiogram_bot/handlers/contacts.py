from aiogram import Router, types
from bot_core.models import Document

router = Router()


@router.message(lambda message: message.text == "Контакты")
async def handle_contacts(message: types.Message):
    contacts_text = (
        "📞 <b>Телефон:</b> +7 (XXX) XXX-XX-XX\n"
        "📧 <b>Почта:</b> rent@example.com\n"
        "📱 <b>Telegram:</b> @rent_company\n"
        "🌐 <b>ВКонтакте:</b> <a href='https://vk.com/rent_company'>vk.com/rent_company</a>\n"
        "📸 <b>Instagram:</b> <a href='https://instagram.com/rent_company'>instagram.com/rent_company</a>"
    )
    back_button = types.KeyboardButton(text="Назад")
    keyboard = types.ReplyKeyboardMarkup(keyboard=[[back_button]], resize_keyboard=True)
    await message.answer(contacts_text, reply_markup=keyboard, parse_mode="HTML")

