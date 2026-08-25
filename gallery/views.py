from django.shortcuts import render
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
