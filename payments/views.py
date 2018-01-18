# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging
from decimal import Decimal

from django.http import Http404
from django.db.models import F
from django.db import transaction

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from payments.helpers import get_balance
from payments.models import Accounts, Transfers, Transactions

# logging.basicConfig()
logger = logging.getLogger(__name__)


class SchemeView(APIView):
    """
    Scheme Post View for authorisation and presentment
    """

    def post(self, request, format=None):
        logger.info("Executing scheme"
                    " view with data - {}".format(request.data))
        data = dict()
        message = ""
        try:
            with transaction.atomic():
                data["cardholder"] = request.data["card_id"]
                request_type = request.data["type"]
                data["billing_amount"] = Decimal(request.data["billing_amount"])
                data["billing_currency"] = request.data["billing_currency"]
                data["transaction_id"] = request.data["transaction_id"]
                data["transaction_currency"] = request.data["transaction_currency"]
                data["transaction_amount"] = Decimal(request.data["transaction_amount"])
                data["merchant_country"] = request.data["merchant_country"]
                data["merchant_name"] = request.data["merchant_name"]
                if request_type == "presentment":
                    data["transfer_status"] = "PR"
                    data["merchant_city"] = request.data["merchant_city"]
                    data["settlement_amount"] = Decimal(request.data["settlement_amount"])
                    data["settlement_currency"] =\
                        request.data["settlement_currency"]
                    logger.info("Creating transfer object")
                    Transfers.objects.create(cardholder=data["cardholder"],
                                             transaction_id=data["transaction_id"],
                                             amount=data["transaction_amount"],
                                             currency=data["transaction_currency"],
                                             transfer_type="DE")
                    logger.info("Updating Account balance")
                    Accounts.objects.filter(cardholder=data["cardholder"])\
                        .update(amount=F('amount') - data["transaction_amount"])
                elif request_type == "authorisation":
                    data["transfer_status"] = "AU"
                    ledger_balance, available_balance \
                        = get_balance(data["cardholder"])
                    if available_balance < data["transaction_amount"]:
                        return Response({"message": "card declined"},
                                        status=status.HTTP_403_FORBIDDEN)
                else:
                    raise Exception("Invalid value for type")
                logger.info("Creating transaction object")
                Transactions.objects.create(**data)
                return Response({"message": "success"},
                                status=status.HTTP_200_OK)
        except KeyError as e:
            logger.error(e.message)
            message = "'{}' is required".format(e.message)
        except Exception as e:
            logger.error(e.message)
            message = "something went wrong, {}".format(e.message)
        return Response({"message": message},
                        status=status.HTTP_400_BAD_REQUEST)

