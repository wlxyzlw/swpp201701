# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-17 02:03
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('omok_backend_rest', '0002_auto_20170416_0851'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='turn',
        ),
        migrations.RemoveField(
            model_name='room',
            name='win',
        ),
    ]