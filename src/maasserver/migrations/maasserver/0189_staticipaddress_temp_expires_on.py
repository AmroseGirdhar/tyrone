# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2019-07-23 02:57
from __future__ import unicode_literals

from django.db import (
    migrations,
    models,
)


class Migration(migrations.Migration):

    dependencies = [
        ('maasserver', '0188_network_testing'),
    ]

    operations = [
        migrations.AddField(
            model_name='staticipaddress',
            name='temp_expires_on',
            field=models.DateTimeField(
                blank=True, editable=False, null=True, db_index=True),
        ),
    ]
