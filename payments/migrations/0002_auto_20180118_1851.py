# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-18 18:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transfers',
            name='transaction_id',
            field=models.CharField(max_length=50, null=True),
        ),
    ]