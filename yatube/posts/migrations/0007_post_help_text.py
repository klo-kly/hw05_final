# Generated by Django 3.2.4 on 2021-06-13 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0006_auto_20210606_1325'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='help_text',
            field=models.TextField(blank=True, verbose_name='Вспомогательный комментарий'),
        ),
    ]