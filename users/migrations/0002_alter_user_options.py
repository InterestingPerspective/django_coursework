# Generated by Django 4.2.5 on 2023-11-05 20:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'permissions': [('set_active', 'Можно блокировать/разблокировать пользователей')], 'verbose_name': 'пользователь', 'verbose_name_plural': 'пользователи'},
        ),
    ]