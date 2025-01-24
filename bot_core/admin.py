from django.contrib import admin
from django.db import transaction

from bot_core.models import UserProfile, Review, Document


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Регистрация в админ панели модели UserProfile."""
    list_display = ['user_id', 'username', 'phone_number', 'registration_date', 'is_admin', 'email']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Регистрация в админ панели модели Review."""
    list_display = ['user', 'text', 'rating']


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    """Регистрация в админ панели модели Document."""
    list_display = ['title', 'file', 'updated_at']


