from django.db import models
from django.contrib.auth.models import User
from PIL import Image
import os


class Profile(models.Model):
    # Связываем профиль с пользователем (один к одному)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    # Аватарка пользователя (загружается в папку avatars/)
    avatar = models.ImageField(
        upload_to='avatars/',
        default='avatars/default.jpg',
        blank=True,
        null=True
    )

    # Биография (по желанию)
    bio = models.TextField(max_length=500, blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    # Метод для автоматического сжатия аватарки (ресайз)
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.avatar and os.path.exists(self.avatar.path):
            img = Image.open(self.avatar.path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.avatar.path)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'