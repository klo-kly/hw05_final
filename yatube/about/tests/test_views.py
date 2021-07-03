from django.test import Client, TestCase
from django.urls.base import reverse


class AboutViewTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_author_page(self):
        """URL, генерируемый при помощи имени '/about/author/', доступен
        неавторизованному пользователю. Используются правильные шаблоны."""
        response = self.guest_client.get(reverse('about:author'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about/author.html')

    def test_tech_page(self):
        """URL, генерируемый при помощи имени '/about/tech/', доступен
        неавторизованному пользователю. Используются правильные шаблоны."""
        response = self.guest_client.get(reverse('about:tech'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about/tech.html')

    def test_tech_page(self):
        """URL, генерируемый при помощи имени '/about/tech/', доступен
        неавторизованному пользователю. Используются правильные шаблоны."""
        response = self.guest_client.get(reverse('about:tech'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about/tech.html')
