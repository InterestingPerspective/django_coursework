from django.core.management import BaseCommand
from django.utils import timezone

from customer.models import Customer
from mailing.models import Mailing, Message


class Command(BaseCommand):
    """Команда для наполнения базы рассылками, клиентами и сообщениями"""
    def handle(self, *args, **options):
        message_list = [
            {'id': 3, 'title': 'Вам понравился заказ?',
             'body': 'Мы передаём все отзывы ответственным командам и постоянно улучшаем сервис, чтобы вы оставались довольны каждой покупкой. Пожалуйста, расскажите ваши впечатления о заказе.'},
            {'id': 2, 'title': 'ТОП книг, которые читают прямо сейчас!', 'body': 'Прямо сейчас этими книгами зачитываются тысячи! Давайте узнаем, в чем же их секрет. Может, это горячие новинки? Или бестселлеры, проверенные временем? Спойлер: всего понемногу, и вам точно стоит их увидеть!'}
        ]
        message_for_create = []

        for message in message_list:
            message_for_create.append(
                Message(**message)
            )

        Message.objects.bulk_create(message_for_create)

        mailing_list = [
            {'mailing_time': timezone.now(), 'periodicity': 1, 'status': 1, 'message': Message.objects.get(pk=2)},
            {'mailing_time': timezone.now(), 'periodicity': 2, 'status': 2, 'message': Message.objects.get(pk=3)},
            {'mailing_time': timezone.now(), 'periodicity': 3, 'status': 1, 'message': Message.objects.get(pk=2)},
            {'mailing_time': timezone.now(), 'periodicity': 1, 'status': 3, 'message': Message.objects.get(pk=3)},
            {'mailing_time': timezone.now(), 'periodicity': 2, 'status': 1, 'message': Message.objects.get(pk=2)},
            {'mailing_time': timezone.now(), 'periodicity': 3, 'status': 3, 'message': Message.objects.get(pk=3)},
            {'mailing_time': timezone.now(), 'periodicity': 1, 'status': 1, 'message': Message.objects.get(pk=2)},
            {'mailing_time': timezone.now(), 'periodicity': 1, 'status': 3},
        ]
        mailing_for_create = []

        for mailing in mailing_list:
            mailing_for_create.append(
                Mailing(**mailing)
            )

        Mailing.objects.bulk_create(mailing_for_create)

        customer_list = [
            {'first_name': 'Ivan', 'last_name': 'Ivanov', 'second_name': 'Ivanovich', 'email': 'testtt_fr2@gmail.com'},
            {'first_name': 'Petr', 'last_name': 'Petrov', 'second_name': 'Petrovich', 'email': 'testtt_fr3@yandex.ru'},
            {'first_name': 'Lev', 'last_name': 'Polevshchikov', 'second_name': 'Anatolievich', 'email': 'tailand.57@yandex.ru'},
            ]
        customer_for_create = []

        for customer in customer_list:
            customer_for_create.append(
                Customer(**customer)
            )

        Customer.objects.bulk_create(customer_for_create)
