from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile
import os
from django.conf import settings

# Список фото (для старта — просто имена файлов)
PHOTOS = [
    "photo1.jpg",
    "photo2.jpg",
    "photo3.jpg",
    "photo4.jpg",
]


def index(request):
    current_index = int(request.GET.get("i", 0))
    if current_index < 0:
        current_index = 0
    if current_index >= len(PHOTOS):
        current_index = len(PHOTOS) - 1

    context = {
        "current_photo": PHOTOS[current_index],
        "prev_index": current_index - 1,
        "next_index": current_index + 1,
        "has_prev": current_index > 0,
        "has_next": current_index < len(PHOTOS) - 1,
    }
    return render(request, "gallery/index.html", context)


@login_required
def profile_view(request):
    # Получаем или создаём профиль для текущего пользователя
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        # Обработка загрузки аватарки
        if 'avatar' in request.FILES:
            profile.avatar = request.FILES['avatar']
            profile.save()
            messages.success(request, 'Аватарка обновлена!')
            return redirect('profile')

        # Обработка изменения биографии
        bio = request.POST.get('bio')
        if bio is not None:
            profile.bio = bio
            profile.save()
            messages.success(request, 'Биография обновлена!')
            return redirect('profile')

    context = {
        'profile': profile,
        'user': request.user,
    }
    return render(request, 'gallery/profile.html', context)
