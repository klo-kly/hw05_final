from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    title = models.CharField(
        max_length=200, verbose_name="Название сообщества"
    )
    slug = models.SlugField(
        max_length=200, unique=True, verbose_name="Адрес страницы"
    )
    description = models.TextField(
        null=True, blank=True, verbose_name="Описание"
    )

    def __str__(self):
        return self.title


class Post(models.Model):
    class Meta:
        ordering = ["-pub_date"]

    group = models.ForeignKey(
        Group, null=True, blank=True,
        verbose_name="Сообщество", related_name="posts",
        on_delete=models.SET_NULL
    )
    text = models.TextField(verbose_name="Текст поста")
    help_text = models.TextField(blank=True,
                                 verbose_name="Вспомогательный комментарий")
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата публикации"
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="posts"
    )
    image = models.ImageField(upload_to="posts/", blank=True, null=True)

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    post = models.ForeignKey(
        Post, related_name="comments",
        on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name="comments"
    )
    text = models.TextField(verbose_name="Текст комментария")
    created = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата комментария"
    )


class Follow(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="follower"
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="following"
    )
