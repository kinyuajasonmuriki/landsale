from django.conf.urls import patterns, include, url
from django.contrib import admin
from marketing.views import * 
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.views.generic import ListView
from marketing.models import *
from django.views.generic import TemplateView
from djgeojson.views import GeoJSONLayerView
from django.contrib.auth import views
from django.contrib.auth import urls

admin.site.site_header = 'LandSale - Online Market'

urlpatterns = patterns('',    	
	url(r'^$', TemplateView.as_view(template_name='devconnect/index.html'), name='index'),
    url(r'^contacts/$','marketing.views.contact', name='contacts'),
    url(r'^register/$', 'marketing.views.register_user', name='register_user'),
    url(r'^buys/', parcelIndex.as_view(), name="buy"),
    url(r'^buy/(?P<slug>\d+)$', parcelDetail.as_view(), name="parcel_detail"),
    #url(r'^map/$', 'marketing.views.map', name='map'),
    url(r'^sell/$','marketing.views.sell', name='sell'),
    url(r'^buyer/$','marketing.views.buyer', name='buyer'),
    url(r'^map/', 'marketing.views.map', name='map'),
    url(r'^parcel_data/$', GeoJSONLayerView.as_view(model=Parcels, properties=('objectid','number','shape_area','designated','sale')), name='parcels'),
    url(r'^buildings_data/$', GeoJSONLayerView.as_view(model=Buildings, properties=('objectid','building_n')), name='buildings'),
    url(r'^boundary_data/$', GeoJSONLayerView.as_view(model=Boundaries, properties=('id')), name='boundary'),
    url(r'^accounts/login/$', 'marketing.views.user_login', name='login'),
    url(r'^accounts/logout/', 'marketing.views.user_logout', name='loggedout'),                                                                                                                    
    url(r'^accounts/', include('registration.backends.simple.urls')),
    #url(r'^register_success/', ('marketing.views.register_success')),
    url(r'^confirm/(?P<activation_key>\w+)/', ('marketing.views.register_confirm')),
    url(r'^password/$', 'django.contrib.auth.views.password_reset', {}, 'password_reset'),
    url(r'^accounts/password_change/$','django.contrib.auth.views.password_change', 
        {'post_change_redirect' : '/accounts/password_change/done/'}, 
        name="password_change"), 
    url(r'^accounts/password_change/done/$','django.contrib.auth.views.password_change_done'),
    url(r'^accounts/password_reset/$', 
        'django.contrib.auth.views.password_reset', 
        {'post_reset_redirect' : '/accounts/password_reset/mailed/'},
        name="password_reset"),
    url(r'^accounts/password_reset/mailed/$',
        'django.contrib.auth.views.password_reset_done'),
    url(r'^accounts/password_reset/(?P<uidb64>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        'django.contrib.auth.views.password_reset_confirm', 
        {'post_reset_redirect' : '/accounts/password_reset/complete/'}),
    url(r'^accounts/password_reset/complete/$', 
        'django.contrib.auth.views.password_reset_complete') 
					    
)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

