from datetime import datetime
from django.conf import settings
from django.db import models
from customer.models import Customer
from users.models import NULLABLE


class Mailing(models.Model):
    TITLE_CHOICES_PERIODICITY = (
        ('daily', 'Раз в день'),
        ('weekly', 'Раз в неделю',),
        ('monthly', 'Раз в месяц',),
    )

    TITLE_CHOICES_STATUS = (
        ('created', 'Создана'),
        ('started', 'Запущена',),
        ('completed', 'Завершена',),
    )

    mailing_time = models.DateTimeField(verbose_name="время рассылки")
    periodicity = models.CharField(max_length=10, verbose_name="периодичность", choices=TITLE_CHOICES_PERIODICITY)
    status = models.CharField(max_length=10, verbose_name='статус рассылки', choices=TITLE_CHOICES_STATUS, default='created')
    title = models.TextField(max_length=100, verbose_name='тема письма')
    body = models.TextField(max_length=350, verbose_name='тело письма')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='пользователь', on_delete=models.CASCADE)
    customers = models.ManyToManyField(Customer, related_name='mailings', verbose_name='клиенты')
    is_active = models.BooleanField(default=True, verbose_name='признак активности')

    def __str__(self):
        return f'Рассылка {self.title}.'

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'

        permissions = [
            (
                'set_active',
                'Можно включать/отключать рассылку'
            ),
        ]


class Log(models.Model):
    STATUS_CHOICES = (
        ('success', 'Успешно'),
        ('failed', 'Не удалось'),
    )

    date_attempt = models.DateTimeField(default=datetime.now, verbose_name='дата попытки')
    status = models.CharField(max_length=150, choices=STATUS_CHOICES, verbose_name='статус попытки')
    answer = models.TextField(**NULLABLE, verbose_name='ответ сервера')
    customers = models.ManyToManyField(Customer, related_name='logs', verbose_name='клиент')
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, related_name='logs', verbose_name='рассылка')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='пользователь')

    def __str__(self):
        return f'Лог: "{self.mailing}"'

    class Meta:
        verbose_name = 'лог'
        verbose_name_plural = 'логи'
