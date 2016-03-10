# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('freebasics', '0002_freebasicstemplatedata'),
    ]

    operations = [
        migrations.RenameField(
            model_name='freebasicstemplatedata',
            old_name='body_background_color',
            new_name='base_background_color',
        ),
        migrations.RenameField(
            model_name='freebasicstemplatedata',
            old_name='body_color',
            new_name='block_background_color',
        ),
        migrations.AddField(
            model_name='freebasicstemplatedata',
            name='block_font_family',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='freebasicstemplatedata',
            name='color',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='freebasicstemplatedata',
            name='text_transform',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='freebasicstemplatedata',
            name='article_position',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='freebasicstemplatedata',
            name='banner_position',
            field=models.IntegerField(default=2),
        ),
        migrations.AlterField(
            model_name='freebasicstemplatedata',
            name='category_position',
            field=models.IntegerField(default=3),
        ),
        migrations.AlterField(
            model_name='freebasicstemplatedata',
            name='footer_position',
            field=models.IntegerField(default=5),
        ),
        migrations.AlterField(
            model_name='freebasicstemplatedata',
            name='header_position',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='freebasicstemplatedata',
            name='poll_position',
            field=models.IntegerField(default=4),
        ),
    ]
