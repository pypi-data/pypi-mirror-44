# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-08-16 16:26
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('saas', '0003_auto_20180713_0601'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='worker',
            options={'permissions': (('view_worker', '\u67e5\u770b\u6210\u5458\u8d44\u6599'),), 'verbose_name': '\u6210\u5458', 'verbose_name_plural': '\u6210\u5458'},
        ),
    ]
