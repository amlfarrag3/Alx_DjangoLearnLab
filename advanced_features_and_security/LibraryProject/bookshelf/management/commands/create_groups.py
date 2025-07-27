from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from bookshelf.models import Book

class Command(BaseCommand):
    help = 'Create default groups and assign permissions'

    def handle(self, *args, **kwargs):
        permissions = {
            'Viewers': ['can_view'],
            'Editors': ['can_view', 'can_create', 'can_edit'],
            'Admins': ['can_view', 'can_create', 'can_edit', 'can_delete'],
        }

        for group_name, perms in permissions.items():
            group, _ = Group.objects.get_or_create(name=group_name)
            for codename in perms:
                try:
                    perm = Permission.objects.get(codename=codename, content_type__app_label='bookshelf')
                    group.permissions.add(perm)
                except Permission.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f"Permission {codename} not found"))
            self.stdout.write(self.style.SUCCESS(f"Group '{group_name}' updated with permissions"))
