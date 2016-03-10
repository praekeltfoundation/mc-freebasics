# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('freebasics', '0003_remove_selected_template_field'),
    ]

    operations = [
        migrations.AlterField(
            model_name='freebasicstemplatedata',
            name='site_name_url',
            field=models.CharField(max_length=255, unique=True, null=True, blank=True),
        ),
    ]