

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Create a new superuser'

    def handle(self, *args, **kwargs):
        username = 'Rohit'  # Replace with the desired new username
        password = 'Ass@.in2211'  # Replace with the desired new password
        email = 'admin@example.com'  # Replace with the desired email

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username, password=password, email=email)
            self.stdout.write(self.style.SUCCESS('Successfully created new superuser'))
        else:
            self.stdout.write(self.style.ERROR('Superuser with this username already exists'))
