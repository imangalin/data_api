from django.core.management.base import BaseCommand

from account.models import Account


class Command(BaseCommand):
    def handle(self, *args, **options):
        Account.objects.all().update(request_day_count=0)
        self.stdout.write(self.style.SUCCESS('Successfully cleared request_day_count in all accounts'))
