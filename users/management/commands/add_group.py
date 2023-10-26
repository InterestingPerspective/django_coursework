from django.contrib.auth.models import Group, Permission
from django.core.management import BaseCommand


class Command(BaseCommand):
    """Команда для наполнения базы группы"""

    def handle(self, *args, **kwargs):

        my_group = Group.objects.create(name='manager_mailing')
        perm = Permission.objects.get(content_type__app_label='customer', content_type__model='customer', codename='add_customer')
        my_group.permissions.add(perm)
        perm = Permission.objects.get(content_type__app_label='customer', content_type__model='customer', codename='view_customer')
        my_group.permissions.add(perm)
        perm = Permission.objects.get(content_type__app_label='customer', content_type__model='customer', codename='delete_customer')
        my_group.permissions.add(perm)
        perm = Permission.objects.get(content_type__app_label='customer', content_type__model='customer', codename='change_customer')
        my_group.permissions.add(perm)

        perm = Permission.objects.get(content_type__app_label='mailing', content_type__model='mailing', codename='add_mailing')
        my_group.permissions.add(perm)
        perm = Permission.objects.get(content_type__app_label='mailing', content_type__model='mailing', codename='view_mailing')
        my_group.permissions.add(perm)
        perm = Permission.objects.get(content_type__app_label='mailing', content_type__model='mailing', codename='delete_mailing')
        my_group.permissions.add(perm)
        perm = Permission.objects.get(content_type__app_label='mailing', content_type__model='mailing', codename='change_mailing')
        my_group.permissions.add(perm)

        my_group = Group.objects.create(name='manager')
        perm = Permission.objects.get(content_type__app_label='mailing', content_type__model='mailing', codename='view_mailing')
        my_group.permissions.add(perm)
        perm = Permission.objects.get(content_type__app_label='customer', content_type__model='customer', codename='view_customer')
        my_group.permissions.add(perm)
        perm = Permission.objects.get(content_type__app_label='mailing', content_type__model='mailing', codename='change_mailing')
        my_group.permissions.add(perm)
        perm = Permission.objects.get(content_type__app_label='customer', content_type__model='customer', codename='change_customer')
        my_group.permissions.add(perm)
