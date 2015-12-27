from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from marketing.models import *
from django.contrib.gis import admin as geoadmin
from leaflet.admin import LeafletGeoAdmin
from django.db.models import signals
from django.core.mail import send_mail
from django.contrib.auth.models import User,Group
from django.db.models import Q
from django.contrib.auth.decorators import login_required, user_passes_test,permission_required
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from django_markdown.admin import MarkdownModelAdmin
from django_markdown.widgets import AdminMarkdownWidget
from django.db.models import TextField

class buildingsAdmin (geoadmin.OSMGeoAdmin):
    list_display = ('objectid','building_n')
    search_fields = ['objectid','building_n'] 

class parcelsAdmin (geoadmin.OSMGeoAdmin):
    list_display = ('objectid','number','shape_area','designated','sale')
    search_fields = ['objectid','sale']
    prepopulated_fields = {"slug": ("objectid",)} 

class boundaryAdmin (geoadmin.OSMGeoAdmin):
    list_display = ('id',)
    search_fields = ['id',] 

class saleAdmin(admin.ModelAdmin):
    pass

class buyAdmin(admin.ModelAdmin):
    pass

admin.site.register(Sale, saleAdmin)
admin.site.register(Buy, buyAdmin)
admin.site.register(Buildings, buildingsAdmin)
admin.site.register(Parcels, parcelsAdmin)
admin.site.register(Boundaries, boundaryAdmin)