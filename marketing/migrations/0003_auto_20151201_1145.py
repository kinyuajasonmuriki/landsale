# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('marketing', '0002_auto_20151201_1126'),
    ]

    operations = [
        migrations.RenameField(
            model_name='parcels',
            old_name='on_sale',
            new_name='sale',
        ),
    ]
