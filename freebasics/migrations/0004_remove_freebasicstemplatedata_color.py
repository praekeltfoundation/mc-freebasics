# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('freebasics', '0003_auto_20160309_1245'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='freebasicstemplatedata',
            name='color',
        ),
    ]
