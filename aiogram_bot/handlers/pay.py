from aiogram import Router, types

router = Router()


@router.message(lambda message: message.text == "Оплатить")
async def handle_pay(message: types.Message):
    rules_text = (
        "Оплата за проживание +79360006256 по этому номеру на имя нашего руководителя(Газпром банк). Алибек Серикович Закупов"
        )
    back_button = types.KeyboardButton(text="Назад")
    keyboard = types.ReplyKeyboardMarkup(keyboard=[[back_button]], resize_keyboard=True)
    await message.answer(rules_text, reply_markup=keyboard)
