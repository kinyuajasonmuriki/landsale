# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import django.contrib.gis.db.models.fields
from django.conf import settings
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Boundaries',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('geom', django.contrib.gis.db.models.fields.MultiLineStringField(srid=4326)),
            ],
        ),
        migrations.CreateModel(
            name='Buildings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('objectid', models.IntegerField()),
                ('shape_leng', models.FloatField()),
                ('shape_area', models.FloatField()),
                ('building_n', models.CharField(max_length=50)),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
            ],
        ),
        migrations.CreateModel(
            name='Buy',
            fields=[
                ('app_id', models.AutoField(serialize=False, primary_key=True)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('id_no', models.IntegerField()),
                ('email', models.EmailField(help_text=b'sale@landsale.com', max_length=50)),
                ('telephone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, null=True, blank=True)),
                ('parcel_no', models.CharField(max_length=50)),
                ('description', models.TextField(max_length=200, null=True, blank=True)),
                ('date_applied', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Parcels',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('objectid', models.IntegerField()),
                ('shape_leng', models.FloatField()),
                ('shape_area', models.FloatField()),
                ('designated', models.CharField(max_length=50)),
                ('on_sale', models.BooleanField(default=False)),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
            ],
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('app_id', models.AutoField(serialize=False, primary_key=True)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('id_no', models.IntegerField()),
                ('email', models.EmailField(help_text=b'sale@landsale.com', max_length=50)),
                ('telephone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, null=True, blank=True)),
                ('parcel_no', models.CharField(max_length=50)),
                ('description', models.TextField(max_length=200, null=True, blank=True)),
                ('date_applied', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('activation_key', models.CharField(max_length=40, blank=True)),
                ('key_expires', models.DateTimeField(default=datetime.date(2015, 12, 1))),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'User profiles',
            },
        ),
        migrations.AddField(
            model_name='buildings',
            name='parcel_no',
            field=models.ForeignKey(to='marketing.Parcels'),
        ),
    ]
