from django.test import TestCase
from django.urls import reverse


class GalleryTests(TestCase):
    def test_homepage_returns_200(self):
        """Проверяем, что главная страница открывается (код 200)"""
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_homepage_uses_correct_template(self):
        """Проверяем, что используется шаблон gallery/index.html"""
        response = self.client.get(reverse('index'))
        self.assertTemplateUsed(response, 'gallery/index.html')  # ← правильный путь!

    def test_homepage_contains_basic_elements(self):
        """Проверяем, что на странице есть ключевые элементы"""
        response = self.client.get(reverse('index'))
        self.assertContains(response, 'Галерея')
        self.assertContains(response, 'DEVOPS')