from django.core.management.base import BaseCommand

from account.models import Account


class Command(BaseCommand):
    def handle(self, *args, **options):
        for account in Account.objects.all():
            account.check_active()
        self.stdout.write(self.style.SUCCESS('Successfully checked all accounts activity status'))
