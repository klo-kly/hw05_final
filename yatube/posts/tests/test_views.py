# deals/tests/test_views.py
import shutil
import tempfile
import time

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse
from django import forms

from ..models import Post, Group, Follow, Comment

User = get_user_model()


class PostsPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        settings.MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)

        cls.user = User.objects.create(username='test_user')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            description='Описание',
            slug='test-slug',
        )
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )
        cls.post = Post.objects.create(
            text='Тестовый текст',
            author=cls.user,
            image=uploaded
        )

        cls.post2 = Post.objects.create(
            text='Тестовый текст',
            author=cls.user,
            group=cls.group,
            image=uploaded
        )

    @classmethod
    def tearDownClass(cls):
        # Модуль shutil - библиотека Python с прекрасными инструментами
        # для управления файлами и директориями:
        # создание, удаление, копирование, перемещение, изменение папок|файлов
        # Метод shutil.rmtree удаляет директорию и всё её содержимое
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.form_fields_new_post = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        self.pages_with_posts = [
            reverse('index'),
            reverse('posts', kwargs={'slug': 'test-slug'})
        ]

    # Проверяем используемые шаблоны
    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_page_names = {
            'index.html': reverse('index'),
            'new_post.html': reverse('new_post'),
            'group.html': reverse('posts', kwargs={'slug': 'test-slug'}),
        }
        for template, reverse_name in templates_page_names.items():
            with self.subTest(template=template):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    # Проверка словаря контекста главной страницы
    def test_home_page_show_correct_context(self):
        """Шаблон index сформирован с правильным контекстом."""
        response = self.guest_client.get(reverse('index'))
        self.assertEqual(response.context.get('page').object_list[1].text,
                         self.post.text)
        self.assertEqual(response.context['page'].object_list[1].image,
                         self.post.image)

    def test_profile_show_correct_context(self):
        """Шаблон profile сформирован с правильным контекстом."""
        response = self.guest_client.get(reverse('profile',
                                                 kwargs={'username': self.user}
                                                 )
                                         )
        self.assertEqual(response.context.get('page').object_list[1].text,
                         self.post.text)
        self.assertEqual(response.context['page'].object_list[1].image,
                         self.post.image)

    def test_post_show_correct_context(self):
        """Шаблон post сформирован с правильным контекстом."""
        response = self.guest_client.get(
            reverse(
                'post',
                kwargs={
                    'username': self.user,
                    'post_id': self.post.id
                }
            )
        )
        self.assertEqual(response.context['post'].image,
                         self.post.image)

    def test_group_page_show_correct_context(self):
        """Шаблон group сформирован с правильным контекстом."""
        response = self.guest_client.get(reverse(
            'posts', kwargs={'slug': 'test-slug'}
        ))
        self.assertEqual(response.context['group'], self.group)
        self.assertEqual(response.context.get('page').object_list[0],
                         self.post2)
        self.assertEqual(response.context['page'].object_list[0].image,
                         self.post2.image)

    def test_new_page_shows_context(self):
        """Шаблон new_post сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('new_post'))
        for value, expected in self.form_fields_new_post.items():
            with self.subTest(value=value):
                form_field = response.context['form'].fields[value]
                self.assertIsInstance(form_field, expected)

    def test_group_pages_not_show_new_post(self):
        """Шаблон group не содержит искомый контекст."""
        response = self.authorized_client.get(
            reverse('posts', kwargs={'slug': 'test-slug'}))
        self.assertTrue(self.post not in response.context['page'])

    def test_page_not_found(self):
        """Сервер возвращает код 404, если страница не найдена."""
        response_page_not_found = self.guest_client.get('/tests_url/')
        self.assertEqual(response_page_not_found.status_code, 404)

    def test_index_page_cash(self):
        response = self.guest_client.get(reverse('index'))
        index_page = response.context.get('page')
        time.sleep(20)
        index_page_cash = response.context.get('page')
        self.assertEqual(index_page, index_page_cash)


class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='Test User')
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)
        for count in range(15):
            cls.post = Post.objects.create(
                text=f'Тестовый пост номер {count}',
                author=cls.user)

    def test_first_page_contains_ten_records(self):
        response = self.authorized_client.get(reverse('index'))
        self.assertEqual(len(response.context.get('page').object_list), 10)

    def test_second_page_contains_three_records(self):
        response = self.authorized_client.get(
            reverse('index') + '?page=2'
        )
        self.assertEqual(len(response.context.get('page').object_list), 5)


class FollowTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.follower = User.objects.create(username='Тестовый подписчик')
        cls.author_1 = User.objects.create(username='Тестовый автор 1')
        cls.follow = Follow.objects.create(author=cls.author_1,
                                           user=cls.follower)
        cls.post = Post.objects.create(
            author=cls.author_1,
            text='Тестовый текст',
        )
        cls.author_2 = User.objects.create(username='Тестовый автор 2')

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client_1 = Client()
        self.authorized_client_1.force_login(FollowTest.follower)
        self.authorized_client_2 = Client()
        self.authorized_client_2.force_login(FollowTest.author_2)

    def test_user_can_follow_author(self):
        """Авторизованный пользователь может
        подписываться на других пользователей."""
        if not Follow.objects.filter(author=FollowTest.author_2,
                                     user=FollowTest.follower).exists():
            self.authorized_client_1.get(reverse(
                'profile_follow', args=[FollowTest.author_2.username]))
        self.assertEqual(Follow.objects.get(user=FollowTest.follower,
                                            author=FollowTest.author_2).author,
                         FollowTest.author_2)

    def test_user_cant_follow_author(self):
        """Неавторизованный не может
        подписываться на других пользователей."""
        if not Follow.objects.filter(author=FollowTest.author_2,
                                     user=FollowTest.follower).exists():
            self.guest_client.get(reverse(
                'profile_follow', args=[FollowTest.author_2.username]))
        self.assertFalse(
            Follow.objects.filter(user=FollowTest.follower,
                                  author=FollowTest.author_2).exists()
        )

    def test_user_can_unfollow_author(self):
        """Авторизованный пользователь может
        удалять других пользователей из подписок."""
        if Follow.objects.filter(author=FollowTest.author_2,
                                 user=FollowTest.follower).exists():
            self.authorized_client_1.get(
                reverse('profile_unfollow',
                        args=[FollowTest.author_2.username]))
        self.assertFalse(Follow.objects.filter(
            user=FollowTest.follower, author=FollowTest.author_2).exists())

    def new_post_appears_tape_follower(self):
        """Новая запись пользователя появляется в ленте тех,
        кто на него подписан."""
        response = self.authorized_client_1.get(reverse('follow_index'))
        self.assertEqual(response.context.get('page')[0].author_1,
                         FollowTest.author_1)

    def new_post_not_appears_tape_not_follower(self):
        """Новая запись пользователя не появляется в ленте тех,
        кто не подписан на него."""
        response = self.authorized_client_1.get(reverse('follow_index'))
        self.assertEqual(response.context.get('page')[0].author_1,
                         FollowTest.author_1)


class CommentTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create(username='Тестовый автор')
        cls.user = User.objects.create(username='Тестовый пользователь')
        cls.post = Post.objects.create(
            author=cls.author,
            text='Тестовый текст',
        )
        cls.comment = Comment.objects.create(
            post=cls.post,
            author=cls.author,
            text='Тестовый комментарий'
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(CommentTest.user)
        self.form_data = {'post': 'Тестовый комментарий'}

    def unauthorized_user_cant_comment(self):
        """Не авторизированный пользователь не может комментировать посты."""
        response = self.guest_client.post(reverse(
            'add_comment', args=[CommentTest.author.username,
                                 CommentTest.post.id]))
        self.assertRedirects(response, reverse(
            'post', args=[CommentTest.author.username,
                          CommentTest.post.id]))

    def authorized_user_can_comment(self):
        """Только авторизированный пользователь может комментировать посты."""
        self.authorized_client.post(reverse(
            'add_comment',
            args=[CommentTest.author.username, CommentTest.post.id]),
            data=self.form_data, follow=True)
        self.assertTrue(
            Comment.objects.filter(post='Тестовый комментарий').exists())
        self.assertTrue(
            Comment.objects.get(post='Тестовый комментарий').text,
            CommentTest.comment.text)
        self.assertTrue(
            Comment.objects.get(post='Тестовый комментарий').author,
            CommentTest.comment.author)
