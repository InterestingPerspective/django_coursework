from django.contrib.auth.models import Group, Permission
from django.core.management import BaseCommand


class Command(BaseCommand):
    """Команда для наполнения базы группы"""

    def handle(self, *args, **kwargs):

        my_group = Group.objects.create(name='user')
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
        perm = Permission.objects.get(content_type__app_label='users', content_type__model='user', codename='view_user')
        my_group.permissions.add(perm)
        perm = Permission.objects.get(content_type__app_label='mailing', content_type__model='mailing', codename='set_active')
        my_group.permissions.add(perm)
        perm = Permission.objects.get(content_type__app_label='users', content_type__model='user', codename='set_active')
        my_group.permissions.add(perm)
