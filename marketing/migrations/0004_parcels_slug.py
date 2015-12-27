# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('marketing', '0003_auto_20151201_1145'),
    ]

    operations = [
        migrations.AddField(
            model_name='parcels',
            name='slug',
            field=models.SlugField(max_length=200, unique=True, null=True),
        ),
    ]
