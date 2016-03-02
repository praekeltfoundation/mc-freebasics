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
                ('siteName', models.CharField(max_length=100, null=True, blank=True)),
                ('siteNameUrl', models.CharField(max_length=100, unique=True, null=True, blank=True)),
                ('bodyBackgroundColor', models.CharField(max_length=100, null=True, blank=True)),
                ('bodyColor', models.CharField(max_length=100, null=True, blank=True)),
                ('bodyFontFamily', models.CharField(max_length=100, null=True, blank=True)),
                ('accent1', models.CharField(max_length=100, null=True, blank=True)),
                ('accent2', models.CharField(max_length=100, null=True, blank=True)),
                ('headerPosition', models.IntegerField(default=1)),
                ('articlePosition', models.IntegerField(default=2)),
                ('bannerPosition', models.IntegerField(default=3)),
                ('categoryPosition', models.IntegerField(default=4)),
                ('pollPosition', models.IntegerField(default=5)),
                ('footerPosition', models.IntegerField(default=6)),
            ],
        ),
    ]
