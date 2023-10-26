from django.db import models
from django.utils import timezone

from users.models import User, NULLABLE


class Message(models.Model):
    title = models.CharField(max_length=150, verbose_name='заголовок')
    body = models.TextField()

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "сообщение"
        verbose_name_plural = 'сообщения'


class Mailing(models.Model):
    TITLE_CHOICES_PERIODICITY = [
        (1, 'Раз в день'),
        (2, 'Раз в неделю',),
        (3, 'Раз в месяц',),
    ]

    TITLE_CHOICES_STATUS = [
        (1, 'Создана'),
        (2, 'Запущена',),
        (3, 'Завершена',),
    ]

    mailing_time = models.DateTimeField(verbose_name="время рассылки", default=timezone.now)
    periodicity = models.PositiveSmallIntegerField(verbose_name="периодичность", choices=TITLE_CHOICES_PERIODICITY,
                                                   default=1)
    status = models.PositiveSmallIntegerField(verbose_name='статус рассылки', choices=TITLE_CHOICES_STATUS, default=1)
    message = models.ForeignKey(Message, on_delete=models.SET_NULL, **NULLABLE)
    user = models.ForeignKey(User, verbose_name='пользователь', on_delete=models.CASCADE, **NULLABLE)

    def __str__(self):
        return f"{self.status}"

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'


class Log(models.Model):
    date_attempt = models.DateTimeField(verbose_name='дата попытки')
    status = models.CharField(max_length=150, verbose_name='статус попытки')
    answer = models.TextField(**NULLABLE, verbose_name='ответ сервера')
    mailing = models.ForeignKey(Mailing, **NULLABLE, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.status} {self.date_attempt}"

    class Meta:
        verbose_name = 'лог'
        verbose_name_plural = 'логи'
