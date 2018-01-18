from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError
from django.db import transaction

from payments.models import Accounts, Transfers


class Command(BaseCommand):
    help = 'Add amount in some currency for an account'

    def add_arguments(self, parser):
        """
        Adding arguments
        """
        parser.add_argument('cardholder', help='card holder or id of the card')
        parser.add_argument('amount', help='Amount to be added')
        parser.add_argument('currency', help='Currency ex: USD')

    def handle(self, *args, **options):
        """
        Handling options and adding accounts and transfer data to db
        """
        try:
            with transaction.atomic():
                # Adding to Accounts
                Accounts.objects.create(
                    cardholder=options.get("cardholder"),
                    amount=options.get("amount"),
                    currency=options.get("currency")
                )
                # Adding to transfer history
                Transfers.objects.create(
                    cardholder=options.get("cardholder"),
                    amount=options.get("amount"),
                    currency=options.get("currency"),
                )
        except IntegrityError:
            raise CommandError('Data already exist for this cardholder')
        self.stdout.write(self.style.SUCCESS('Successfully loaded money for the cardholder'))