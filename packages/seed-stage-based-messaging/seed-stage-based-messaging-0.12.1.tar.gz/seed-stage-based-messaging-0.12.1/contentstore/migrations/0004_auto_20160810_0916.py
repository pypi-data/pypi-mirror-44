# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-08-10 09:16
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("contentstore", "0003_auto_20160513_1115")]

    operations = [
        migrations.AlterField(
            model_name="message",
            name="binary_content",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="message",
                to="contentstore.BinaryContent",
            ),
        )
    ]
