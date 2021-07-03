from django.contrib.auth import get_user_model
from django.test import TestCase
from ..models import Post, Group

User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(username='Каля')
        cls.post = Post.objects.create(text='ж' * 100, author=cls.user)

    def test_text_return_str(self):
        """правильный вывод при обращение к методу __str__"""
        self.assertEqual(str(PostModelTest.post), PostModelTest.post.text[:15])


class GroupModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = Group.objects.create(title='ж' * 100, slug='/')

    def test_text_return_str(self):
        """правильный вывод при обращение к методу __str__"""
        self.assertEqual(str(GroupModelTest.group), GroupModelTest.group.title)
