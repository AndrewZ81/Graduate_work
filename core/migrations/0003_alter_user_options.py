# Generated by Django 4.1.6 on 2023-03-16 19:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_user_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'Пользователь Web-приложения TodoList', 'verbose_name_plural': 'Пользователи Web-приложения TodoList'},
        ),
    ]