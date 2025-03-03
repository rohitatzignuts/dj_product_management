from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = "Seed an admin user"

    def handle(self, *args, **kwargs):
        username = "rohit"
        email = "rohitv@zignuts.com"
        password = "test@132"

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(
                username=username, email=email, password=password
            )
            self.stdout.write(
                self.style.SUCCESS(f"Admin user '{username}' created successfully!")
            )
        else:
            self.stdout.write(
                self.style.WARNING(f"Admin user '{username}' already exists.")
            )
