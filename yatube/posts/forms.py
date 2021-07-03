from django import forms

from .models import Comment, Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['text', 'group', 'image']
        help_texts = {
            'text': ('Это поле для ввода текста Вашей записи.'),
            'group': ('Это сообщество в котором опубликуется запись.'),
            'image': ('Это поле для загрузки картинки.')
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text',]
        help_texts = {
            'text': ('Это поле для ввода текста Вашего комментария.'),
            }
