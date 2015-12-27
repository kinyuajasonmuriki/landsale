from django.db import models
from django.contrib.gis.db import models
import datetime 
from django.utils import timezone
from django.db.models import signals
from django.forms import TextInput
from django.contrib.auth.models import User,Group
from django.core.validators import MaxLengthValidator,MinLengthValidator
from django.template.defaultfilters import date
from django.core.urlresolvers import reverse
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class UserProfile(models.Model):
	
	user = models.OneToOneField(User)
	activation_key = models.CharField(max_length=40, blank=True)
	key_expires = models.DateTimeField(default=datetime.date.today()) 
	
	def __str__(self):
		return self.user.username

	class Meta:
		verbose_name_plural='User profiles'
		managed = True

class Buildings(models.Model):
	objectid = models.IntegerField()
	shape_leng = models.FloatField()
	shape_area = models.FloatField()
	building_n = models.CharField(max_length=50)
	parcel_no = models.ForeignKey('Parcels', null=True,blank=True)
	geom = models.MultiPolygonField(srid=4326)
	objects = models.GeoManager()

	def __unicode__(self):
		return unicode(self.building_n)

	class Meta:
		verbose_name_plural='Buildings Data'
		managed = True


class Parcels(models.Model):
	objectid = models.IntegerField()
	shape_leng = models.FloatField()
	shape_area = models.FloatField()
	designated = models.CharField(max_length=50)
	number = models.CharField(max_length=50, null=True, blank=True)
	sale = models.BooleanField(default=False)
	slug = models.SlugField(max_length=200, unique=True, null=True)
	geom = models.MultiPolygonField(srid=4326)
	objects = models.GeoManager()

	def __unicode__(self):
		return unicode(self.number)

	def get_absolute_url(self):
		return reverse("parcel_detail", kwargs={"slug": self.slug})

	def get_developers_count(self):
		return self.Developer.count()

	class Meta:
		verbose_name_plural='Parcel Data'
		managed = True	

	


class Boundaries(models.Model):
	id = models.IntegerField(primary_key=True)
	geom = models.MultiLineStringField(srid=4326)
	objects = models.GeoManager()

	def __unicode__(self):
		return unicode(self.id)

	class Meta:
		verbose_name_plural='Registration Boundary'
		managed = True

class Sale(models.Model):
	user = models.OneToOneField(User, unique=False)
	app_id=models.AutoField(primary_key=True)
	first_name=models.CharField(max_length=50)
	last_name=models.CharField(max_length=50)
	id_no = models.IntegerField()
	email = models.EmailField(max_length=50, help_text='sale@landsale.com')
	telephone = PhoneNumberField(null=True,blank=True)
	parcel_no = models.CharField(max_length=50)
	description = models.TextField(max_length=200,null=True, blank=True)
	date_applied = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return unicode(self.id_no)

	class Meta:
		verbose_name_plural='Land Sales'
		managed = True


class Buy(models.Model):
	app_id=models.AutoField(primary_key=True)
	first_name=models.CharField(max_length=50)
	last_name=models.CharField(max_length=50)
	id_no = models.IntegerField()
	email = models.EmailField(max_length=50, help_text='sale@landsale.com')
	telephone = PhoneNumberField(null=True,blank=True)
	parcel_no = models.CharField(max_length=50)
	description = models.TextField(max_length=200,null=True, blank=True)
	date_applied = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return unicode(self.id_no)

	class Meta:
		verbose_name_plural='Land Purchases'
		managed = True


