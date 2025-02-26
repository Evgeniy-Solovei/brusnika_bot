from aiogram.types import KeyboardButton, WebAppInfo
from aiogram.utils.keyboard import ReplyKeyboardBuilder


async def get_main_keyboard():
    # Создаем кнопки
    buttons = [
        KeyboardButton(text="Забронировать",
                       web_app=WebAppInfo(url="https://realtycalendar.ru/booking-widget/00e320c273dd70b276b78cd2ba5a91ae")),
        KeyboardButton(text="Оплатить"),
        KeyboardButton(text="Правила заселения"),
        KeyboardButton(text="Бесконтактное заселение"),
        KeyboardButton(text="Договор аренды"),
        KeyboardButton(text="Контакты"),
        KeyboardButton(text="Часто задаваемые вопросы"),
        KeyboardButton(text="Оставить отзыв")
    ]
    builder = ReplyKeyboardBuilder()
    builder.add(*buttons)
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)
