import datetime

from django.core.mail import send_mail
from django.core.management import BaseCommand

from mailing.models import Mailing, Log


class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        mailings = Mailing.objects.all()
        logs = Log.objects.all()
        time = datetime.datetime.now().replace(tzinfo=None)

        for mailing in mailings:

            if self.get_info_for_mailing_start(mailing, logs, time):
                related_customers = mailing.customers.all()

                if len(related_customers) == 0:
                    log = Log.objects.create(
                        status='failed',
                        mailing=mailing,
                        answer='Отсутсвуют клиенты для рассылки.',
                        user=mailing.user,
                    )
                    log.save()
                    break

                for customer in related_customers:

                    try:
                        status = send_mail(
                            mailing.title,
                            mailing.body,
                            None,
                            [customer.email],
                            fail_silently=False
                        )
                        mailing.status = 'started'
                        mailing.save()
                    except ConnectionRefusedError as error:
                        log = Log.objects.create(
                            date_attempt=time,
                            status='failed',
                            mailing=mailing,
                            answer=error,
                            user=mailing.user,
                        )
                        log.customer.set([customer])
                        log.save()
                        mailing.status = 'created'
                        mailing.save()
                    else:

                        if status:
                            log = Log.objects.create(
                                date_attempt=time,
                                status='success',
                                mailing=mailing,
                                user=mailing.user,
                            )
                            log.customer.set([customer])
                            log.save()
                            mailing.status = 'completed'
                            mailing.save()
                        else:
                            log = Log.objects.create(
                                date_attempt=time,
                                status='failed',
                                mailing=mailing,
                                user=mailing.user,
                            )
                            log.customer.set([customer])
                            log.save()
                            mailing.status = 'created'
                            mailing.save()

            else:
                continue

    @staticmethod
    def get_info_for_mailing_start(mailing, logs, time):
        mailing_latest_log = logs.filter(mailing=mailing).all().order_by('-date_attempt').first()

        if mailing_latest_log is None:

            if not mailing.is_active:
                return False

            elif mailing.mailing_time.replace(
                    hour=0,
                    minute=0,
                    second=0,
                    microsecond=0,
                    tzinfo=None
            ) <= time:
                return True

        elif not mailing.is_active:
            return False

        elif mailing_latest_log.status == 'failed':
            return True

        else:

            log_time = mailing_latest_log.date_attempt.replace(
                hour=0,
                minute=0,
                second=0,
                microsecond=0,
                tzinfo=None
            )
            time_difference = (time - log_time).days

            if mailing.periodicity == 'daily':

                if time_difference == 1:
                    return True

            elif mailing.periodicity == 'weekly':

                if time_difference == 7:
                    return True

            else:

                if time_difference == 30:
                    return True
