from django.core.management.base import BaseCommand

from account.models import Account


class Command(BaseCommand):
    def handle(self, *args, **options):
        for account in Account.objects.all():
            account.clear_month_count()
        self.stdout.write(self.style.SUCCESS('Monthly count successfully cleaned'))
