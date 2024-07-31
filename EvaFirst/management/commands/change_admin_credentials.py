# F/management/commands/change_admin_credentials.py

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

User = get_user_model()

class Command(BaseCommand):
    help = 'Change admin username and password'

    def handle(self, *args, **kwargs):
        old_username = 'JD'  # Replace with current admin username
        new_username = 'Rohit'  # Replace with new admin username
        new_password = 'Ass'  # Replace with new admin password

        try:
            user = User.objects.get(username=old_username)
            user.username = new_username
            user.set_password(new_password)
            user.save()
            self.stdout.write(self.style.SUCCESS('Successfully updated admin credentials'))
        except ObjectDoesNotExist:
            self.stdout.write(self.style.ERROR(f'User with username "{old_username}" does not exist'))


        # try:

        # except User.DoesNotExist:
        #     self.stdout.write(self.style.ERROR('Admin user does not exist'))
