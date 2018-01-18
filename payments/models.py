# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from payments.constants import TRANSFER_CHOICES, TRANSFER_STATUS_CHOICES


class Accounts(models.Model):
    """
    Holds the monetary value in some currency
    """
    cardholder = models.CharField(max_length=32, unique=True)
    amount = models.DecimalField(max_digits=50, decimal_places=5)
    currency = models.CharField(max_length=5)

    class Meta:
        verbose_name_plural = "Accounts"


class Transfers(models.Model):
    """
    Holds the transfer history
    """

    cardholder = models.CharField(max_length=32)
    transaction_id = models.CharField(max_length=50, null=True)
    amount = models.DecimalField(max_digits=50, decimal_places=5)
    currency = models.CharField(max_length=5)
    transferred_on = models.DateTimeField(auto_now_add=True)
    transfer_type = models.CharField(
        max_length=2,
        choices=TRANSFER_CHOICES,
        default='CR',
    )

    class Meta:
        verbose_name_plural = "Transfers"


class Transactions(models.Model):
    """
    Holds the Transaction history
    """
    cardholder = models.CharField(max_length=32)
    transaction_id = models.CharField(max_length=50)
    billing_amount = models.DecimalField(max_digits=50, decimal_places=5)
    billing_currency = models.CharField(max_length=5)
    transaction_amount = models.DecimalField(max_digits=50, decimal_places=5)
    transaction_currency = models.CharField(max_length=5)
    settlement_amount = models.DecimalField(max_digits=50, decimal_places=5, null=True)
    settlement_currency = models.CharField(max_length=5, null=True)
    transferred_on = models.DateTimeField(auto_now_add=True)
    transfer_status = models.CharField(
        max_length=2,
        choices=TRANSFER_STATUS_CHOICES,
        default='PR',
    )
    merchant_name = models.CharField(max_length=100, null=True)
    merchant_country = models.CharField(max_length=3, null=True)
    merchant_mcc = models.CharField(max_length=20, null=True)
    merchant_city = models.CharField(max_length=20, null=True)

    class Meta:
        verbose_name_plural = "Transactions"





