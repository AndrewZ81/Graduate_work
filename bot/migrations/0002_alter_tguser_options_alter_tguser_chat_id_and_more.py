# Generated by Django 4.1.6 on 2023-03-16 19:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bot', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tguser',
            options={'verbose_name': 'Пользователь Telegram', 'verbose_name_plural': 'Пользователи Telegram'},
        ),
        migrations.AlterField(
            model_name='tguser',
            name='chat_id',
            field=models.BigIntegerField(unique=True, verbose_name='Chat ID Телеграм'),
        ),
        migrations.AlterField(
            model_name='tguser',
            name='user',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь Web-приложения TodoList'),
        ),
        migrations.AlterField(
            model_name='tguser',
            name='verification_code',
            field=models.CharField(blank=True, default=None, max_length=30, null=True, verbose_name='Код верификации бота'),
        ),
    ]
