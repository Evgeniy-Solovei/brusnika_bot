from aiogram import types, F, Router, Bot
from aiogram.exceptions import TelegramAPIError
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from django.core.mail import send_mail
from bot_core.models import UserProfile, Review

router = Router()


# Обработчик команды "Оставить отзыв"
@router.message(F.text == "Оставить отзыв")
async def handle_review_start(message: types.Message):
    # Просим пользователя написать отзыв
    await message.answer("Напишите ваш отзыв:", reply_markup=ReplyKeyboardRemove())


# Обработчик текста отзыва
@router.message()
async def handle_review_text(message: types.Message):
    # Получаем текст отзыва
    text = message.text

    # Получаем или создаём профиль пользователя
    user, created = await UserProfile.objects.aget_or_create(
        user_id=message.from_user.id,
        defaults={"username": message.from_user.username}
    )

    # Сохраняем отзыв в базу данных
    await Review.objects.acreate(user=user, text=text)
    # Возвращаем пользователя в главное меню с кнопкой "Назад"
    back_button = KeyboardButton(text="Назад")
    keyboard = ReplyKeyboardMarkup(keyboard=[[back_button]], resize_keyboard=True)
    await message.answer("Спасибо за ваш отзыв!", reply_markup=keyboard)

    # Отправляем письмо на почту
    admin_emails = [admin.email async for admin in UserProfile.objects.filter(is_admin=True).aiterator()]
    send_mail(
        subject="Новый отзыв",
        message=f"Пользователь: @{user.username if user.username else user.user_id}\nТекст: {text}",
        from_email="e.v.solovey@inbox.ru",
        recipient_list=admin_emails,  # Список email администраторов
        fail_silently=False,
    )
