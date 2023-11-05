from django.contrib import admin

from mailing.models import Mailing, Log


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('mailing_time', 'periodicity', 'status', 'title', 'body')


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('date_attempt', 'status', 'answer')
