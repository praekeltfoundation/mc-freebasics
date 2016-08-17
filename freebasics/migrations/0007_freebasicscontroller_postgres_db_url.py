# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('freebasics', '0006_change_site_url_field_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='freebasicscontroller',
            name='postgres_db_url',
            field=models.TextField(null=True, blank=True),
        ),
    ]
