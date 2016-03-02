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
            old_name='articlePosition',
            new_name='article_position',
        ),
        migrations.RenameField(
            model_name='freebasicstemplatedata',
            old_name='bannerPosition',
            new_name='banner_position',
        ),
        migrations.RenameField(
            model_name='freebasicstemplatedata',
            old_name='bodyBackgroundColor',
            new_name='body_background_color',
        ),
        migrations.RenameField(
            model_name='freebasicstemplatedata',
            old_name='bodyColor',
            new_name='body_color',
        ),
        migrations.RenameField(
            model_name='freebasicstemplatedata',
            old_name='bodyFontFamily',
            new_name='body_font_family',
        ),
        migrations.RenameField(
            model_name='freebasicstemplatedata',
            old_name='categoryPosition',
            new_name='category_position',
        ),
        migrations.RenameField(
            model_name='freebasicstemplatedata',
            old_name='footerPosition',
            new_name='footer_position',
        ),
        migrations.RenameField(
            model_name='freebasicstemplatedata',
            old_name='headerPosition',
            new_name='header_position',
        ),
        migrations.RenameField(
            model_name='freebasicstemplatedata',
            old_name='pollPosition',
            new_name='poll_position',
        ),
        migrations.RenameField(
            model_name='freebasicstemplatedata',
            old_name='siteNameUrl',
            new_name='site_name',
        ),
        migrations.RemoveField(
            model_name='freebasicstemplatedata',
            name='siteName',
        ),
        migrations.AddField(
            model_name='freebasicstemplatedata',
            name='site_name_url',
            field=models.CharField(max_length=100, unique=True, null=True, blank=True),
        ),
    ]
