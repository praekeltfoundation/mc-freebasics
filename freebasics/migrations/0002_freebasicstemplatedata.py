# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('freebasics', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FreeBasicsTemplateData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('site_name', models.CharField(max_length=100, unique=True, null=True, blank=True)),
                ('site_name_url', models.URLField(max_length=255, unique=True, null=True, blank=True)),
                ('body_background_color', models.CharField(max_length=100, null=True, blank=True)),
                ('body_color', models.CharField(max_length=100, null=True, blank=True)),
                ('body_font_family', models.CharField(max_length=100, null=True, blank=True)),
                ('accent1', models.CharField(max_length=100, null=True, blank=True)),
                ('accent2', models.CharField(max_length=100, null=True, blank=True)),
                ('header_position', models.IntegerField(default=1)),
                ('article_position', models.IntegerField(default=2)),
                ('banner_position', models.IntegerField(default=3)),
                ('category_position', models.IntegerField(default=4)),
                ('poll_position', models.IntegerField(default=5)),
                ('footer_position', models.IntegerField(default=6)),
                ('controller', models.OneToOneField(to='freebasics.FreeBasicsController')),
            ],
        ),
    ]
