import asyncio
import logging
from asyncio import to_thread
from aiogram import types, F, Router, Bot
from aiogram.exceptions import TelegramAPIError
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from django.core.mail import send_mail
from bot_core.models import UserProfile, Review

router = Router()
logger = logging.getLogger(__name__)


# Обработчик команды "Оставить отзыв"
# Создаём состояния для отзыва
class ReviewState(StatesGroup):
    waiting_for_text = State()  # Ожидание текста отзыва
    waiting_for_rating = State()  # Ожидание рейтинга


# Обработчик команды "Оставить отзыв"
@router.message(F.text == "Оставить отзыв")
async def handle_review_start(message: types.Message, state: FSMContext):
    # Переводим пользователя в состояние ожидания текста отзыва
    await state.set_state(ReviewState.waiting_for_text)
    await message.answer("Напишите ваш отзыв:", reply_markup=ReplyKeyboardRemove())


# Обработчик текста отзыва
@router.message(ReviewState.waiting_for_text)
async def handle_review_text(message: types.Message, state: FSMContext):
    # Сохраняем текст отзыва в состояние
    await state.update_data(text=message.text)
    # Переводим пользователя в состояние ожидания рейтинга
    await state.set_state(ReviewState.waiting_for_rating)
    await message.answer("Оцените нас от 1 до 5:")


# Обработчик рейтинга
@router.message(ReviewState.waiting_for_rating)
async def handle_review_rating(message: types.Message, state: FSMContext, bot: Bot):
    # Проверяем, что рейтинг — это число от 1 до 5
    try:
        rating = int(message.text)
        if rating < 1 or rating > 5:
            raise ValueError
    except ValueError:
        await message.answer("Пожалуйста, введите число от 1 до 5.")
        return
    # Получаем текст отзыва из состояния
    data = await state.get_data()
    text = data.get("text")

    # Получаем или создаём профиль пользователя
    user, created = await UserProfile.objects.aget_or_create(user_id=message.from_user.id,
                                                             defaults={"username": message.from_user.username})

    # Сохраняем отзыв в базу данных
    await Review.objects.acreate(user=user, text=text, rating=rating)
    # Сбрасываем состояние
    await state.clear()
    # Возвращаем пользователя в главное меню
    back_button = KeyboardButton(text="Назад")
    keyboard = ReplyKeyboardMarkup(keyboard=[[back_button]], resize_keyboard=True)
    await message.answer("Спасибо за ваш отзыв!", reply_markup=keyboard)
    async for admin in UserProfile.objects.filter(is_admin=True).aiterator():
        try:
            await bot.send_message(
                chat_id=admin.user_id,
                text=f"Новый отзыв!\n\nПользователь: @{user.username if user.username else user.user_id}\nРейтинг: {rating}\nТекст: {text}"
            )
        except TelegramAPIError as e:
            print(f"Не удалось отправить сообщение администратору {admin.user_id}: {e}")

    # Отправляем письмо на почту
    admin_emails = [admin.email async for admin in UserProfile.objects.filter(is_admin=True).aiterator()]

    logger.info(f"Attempting to send email to: {admin_emails}")

    if not admin_emails:
        logger.warning("No admin emails found in database!")
        return
    try:
        # Явно передаем все параметры для send_mail
        logger.debug("Sending test email...")
        await to_thread(
            send_mail,
            subject="Новый отзыв",
            message=f"Пользователь: @{user.username if user.username else user.user_id}\nТекст: {text}",
            from_email="e.v.solovey@inbox.ru",
            recipient_list=admin_emails,
            html_message=None,
            fail_silently=False,
            auth_user=None,  # Явно указываем None если используем настройки Django
            auth_password=None,
            connection=None
        )
        logger.info("Test email sent successfully")
    except Exception as e:
        logger.error(f"Test email failed: {str(e)}", exc_info=True)
