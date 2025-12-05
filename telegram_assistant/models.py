# telegram_assistant/models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class TelegramSession(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='telegram_session'
    )
    logged_in = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"TG Session {self.user.username} — {'Logged' if self.logged_in else 'Not logged'}"

    class Meta:
        verbose_name = "Telegram сессия"
        verbose_name_plural = "Telegram сессии"