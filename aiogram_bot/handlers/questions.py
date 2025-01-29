from aiogram import Router, types, F
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder


router = Router()


faq_data = [
    {"question": "Как могу получить ключи?", "answer": "Заселение происходит дистанционно (бесконтактно). Рядом с дверью квартиры установлен бокс для ключей. После подтверждения бронирования, вам передаётся вся необходимая информация – код домофона, код от кейбокса. Это очень удобно и позволяет Вам заселиться в удобное для вас время, круглосуточно."},
    {"question": "Могу ли заехать пораньше?", "answer": "К сожалению, гарантировать ранний заезд не можем, так как до 12:00 там имеют право проживать предыдущие гости(если они будут там проживать). Точно можно будет узнать только в день заезда. Позвоните нам, пожалуйста, с утра, и мы уточним по Вашему вопросу. Либо сами бронируете на сутки ранее, в таком случае квартира не будет заселена и вы сможете заехать с утра."},
    {"question": "Могу ли выехать на несколько часов позже?", "answer": "Поздний выезд по возможности, если нет брони. Оплачивается дополнительно. До 17:00 – стоимость 50% от стоимости суток, после 17:00 стоимость полных суток, либо 350 руб/час."},
    {"question": "Во сколько могу заехать?", "answer": "Официальный заезд с 14:00, расчетный час до 12:00."},
    {"question": "Предоставляете ли отчётные документы?", "answer": "Предоставляем полностью все отчётные документы (акт, договор, фискальный чек).\nБухгалтерия:\nEmail: brusnika.holding@yandex.ru"},
    {"question": "Когда мне вернут залог?", "answer": "В день Вашего выезда горничная приходит, проверяет квартиру и после этого возвращаем залог. Время возврата – в течении дня.(Иногда, возможны задержки на стороне банка)"},
]


# Создаём класс для колбэков
class FAQCallback(CallbackData, prefix="faq"):
    question_id: int  # ID вопроса


@router.message(F.text == "Часто задаваемые вопросы")
async def handle_faq(message: types.Message):
    # Создаём клавиатуру с вопросами
    builder = InlineKeyboardBuilder()
    for index, item in enumerate(faq_data):
        builder.button(text=item["question"], callback_data=FAQCallback(question_id=index).pack())
    builder.adjust(1)
    # Добавляем кнопку "Назад"
    back_button = types.KeyboardButton(text="Назад")
    keyboard = types.ReplyKeyboardMarkup(keyboard=[[back_button]], resize_keyboard=True)

    # Отправляем сообщение с вопросами
    await message.answer("Выберите вопрос:", reply_markup=builder.as_markup())


@router.callback_query(FAQCallback.filter())
async def handle_faq_callback(callback: types.CallbackQuery, callback_data: FAQCallback):
    # Получаем ID вопроса
    question_id = callback_data.question_id
    # Отправляем ответ на вопрос
    if 0 <= question_id < len(faq_data):
        answer = faq_data[question_id]["answer"]
        await callback.message.answer(answer)
    else:
        await callback.message.answer("Вопрос не найден.")
    # Подтверждаем обработку колбэка
    await callback.answer()
