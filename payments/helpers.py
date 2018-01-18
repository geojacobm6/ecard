import datetime
import logging

from django.db.models import Sum

from payments.models import Accounts, Transfers, Transactions


# logging.basicConfig()
logger = logging.getLogger(__name__)


def get_balance(card_id):
    """
    Getting ledger and available balance for last 2 days of period
    :param card_id:
    :return: ledger_balance, available_balance
    """
    logger.info("Getting Balance")
    ledger_balance = Accounts.objects.get(cardholder=card_id).amount
    transfer_period = datetime.datetime.now() - datetime.timedelta(days=2)
    transfers = list(set(Transfers.objects.filter(cardholder=card_id,
                                                  transferred_on__gte=transfer_period,
                                                  transaction_id__isnull=False)
                         .values_list("transaction_id", flat=True)))
    transactions = Transactions.objects.filter(cardholder=card_id,
                                               transferred_on__gte=transfer_period,
                                               transfer_status="AU")\
        .exclude(transaction_id__in=transfers).aggregate(authorised_total=Sum('transaction_amount'))
    logger.info("transactions is {}".format(transactions))
    if transactions["authorised_total"]:
        available_balance = ledger_balance - transactions["authorised_total"]
    else:
        available_balance = ledger_balance
    logger.info("Ledger - {},"
                " Available - {}".format(ledger_balance,
                                         available_balance))
    return ledger_balance, available_balance
