import os
from aiogram import Router, types
from aiogram.types import FSInputFile

router = Router()


@router.message(lambda message: message.text == "Бесконтактное заселение")
async def handle_contactless_check_in(message: types.Message):
    print("Текущая рабочая директория:", os.getcwd())
    text = (
        "Заселение происходит дистанционно (бесконтактно). Рядом с дверью квартиры установлен бокс для ключей. После "
        "подтверждения бронирования, вам передаётся вся необходимая информация – код домофона, код от кейбокса. "
        "Это очень удобно и позволяет Вам заселиться в удобное для вас время, круглосуточно."
    )
    back_button = types.KeyboardButton(text="Назад")
    keyboard = types.ReplyKeyboardMarkup(keyboard=[[back_button]], resize_keyboard=True)
    await message.answer(text, reply_markup=keyboard)

    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    photo1_path = os.path.join(base_path, 'agreements', '1.png')
    photo2_path = os.path.join(base_path, 'agreements', '2.png')
    print("Путь нахуй:", base_path)
    print("Путь к первому фото:", photo1_path)
    print("Путь ко второму фото:", photo2_path)
    if not os.path.exists(photo1_path):
        raise FileNotFoundError(f"Файл {photo1_path} не найден.")
    if not os.path.exists(photo2_path):
        raise FileNotFoundError(f"Файл {photo2_path} не найден.")
    photo1 = FSInputFile(photo1_path)
    await message.answer_photo(photo=photo1)
    photo2 = FSInputFile(photo2_path)
    await message.answer_photo(photo=photo2)

