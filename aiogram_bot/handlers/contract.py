from aiogram import Router, types
from aiogram.types import FSInputFile

from bot_core.models import Document

router = Router()


@router.message(lambda message: message.text == "Договор аренды")
async def handle_rules(message: types.Message):
    # Получаем документ из базы данных, первый документ
    document = await Document.objects.afirst()
    if document and document.file:
        # Получаем путь к файлу
        file_path = document.file.path

        # Создаем объект FSInputFile
        input_file = FSInputFile(file_path)

        # Отправляем текст и кнопку "Назад"
        rules_text = "Ознакомьтесь с договором ⬇️"
        back_button = types.KeyboardButton(text="Назад")
        keyboard = types.ReplyKeyboardMarkup(keyboard=[[back_button]], resize_keyboard=True)

        # Отправляем документ пользователю
        await message.answer(rules_text, reply_markup=keyboard)
        await message.answer_document(input_file)
    else:
        # Если документа нет в базе данных
        await message.answer("Документ не найден.")

