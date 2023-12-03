from django.core.management import BaseCommand

from user_auth.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            email='frausonya131@gmail.com',
            first_name='Admin',
            last_name='Mailing',
            is_staff=True,
            is_superuser=True,
            is_active=True
        )

        user.set_password('123qwe456rty')
        user.save()
