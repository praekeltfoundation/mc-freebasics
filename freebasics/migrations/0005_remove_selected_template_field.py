# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('freebasics', '0004_remove_freebasicstemplatedata_color'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='freebasicscontroller',
            name='selected_template',
        ),
    ]
