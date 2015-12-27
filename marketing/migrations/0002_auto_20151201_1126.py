# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('marketing', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='boundaries',
            options={'managed': True, 'verbose_name_plural': 'Registration Boundary'},
        ),
        migrations.AlterModelOptions(
            name='buildings',
            options={'managed': True, 'verbose_name_plural': 'Buildings Data'},
        ),
        migrations.AlterModelOptions(
            name='buy',
            options={'managed': True, 'verbose_name_plural': 'Land Purchases'},
        ),
        migrations.AlterModelOptions(
            name='parcels',
            options={'managed': True, 'verbose_name_plural': 'Parcel Data'},
        ),
        migrations.AlterModelOptions(
            name='sale',
            options={'managed': True, 'verbose_name_plural': 'Land Sales'},
        ),
        migrations.AlterModelOptions(
            name='userprofile',
            options={'managed': True, 'verbose_name_plural': 'User profiles'},
        ),
        migrations.AddField(
            model_name='parcels',
            name='number',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='buildings',
            name='parcel_no',
            field=models.ForeignKey(blank=True, to='marketing.Parcels', null=True),
        ),
    ]
