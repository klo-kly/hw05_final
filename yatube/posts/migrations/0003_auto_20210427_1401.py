# Generated by Django 2.2.9 on 2021-04-27 11:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='posts.Group', verbose_name='Сообщество'),
        ),
        migrations.AlterField(
            model_name='group',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='post',
            name='pub_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации'),
        ),
        migrations.AlterField(
            model_name='post',
            name='text',
            field=models.TextField(verbose_name='Текст поста'),
        ),
    ]
