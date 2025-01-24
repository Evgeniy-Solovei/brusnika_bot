from django.db import models


class UserProfile(models.Model):
    """Профиль пользователя"""
    user_id = models.BigIntegerField(unique=True, verbose_name="ID пользователя в Telegram")
    username = models.CharField(max_length=255, null=True, blank=True, verbose_name="Имя пользователя")
    phone_number = models.CharField(max_length=20, null=True, blank=True, verbose_name="Номер телефона")
    registration_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата регистрации игрока")
    is_admin = models.BooleanField(default=False, verbose_name="Администратор системы")
    email = models.EmailField(null=True, blank=True, unique=True, verbose_name='Почта')

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        if self.username:
            return f"{self.user_id} ({self.username})"
        if self.user_id is not None:
            return str(self.user_id)
        return "Без имени и ID"


class Review(models.Model):
    """Отзыв"""
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="Пользователь")
    text = models.TextField(null=True, blank=True, verbose_name="Текст отзыва")
    rating = models.PositiveIntegerField(null=True, blank=True, verbose_name="Рейтинг")

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"


class Document(models.Model):
    """Документ для пользователей"""
    title = models.CharField(null=True, blank=True, max_length=50, verbose_name="Название соглашения")
    file = models.FileField(null=True, blank=True, upload_to='agreements/', verbose_name="Файл соглашения")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Договор аренды"
        verbose_name_plural = "Договор аренды"

    def __str__(self):
        return self.title
