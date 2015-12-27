from marketing.forms import *
from marketing.models import *
from django.shortcuts import render_to_response, HttpResponseRedirect, render
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.gis.geos import Point
from django.core.context_processors import csrf
import uuid
from django.views import generic
from django.shortcuts import render_to_response, get_object_or_404
from django.utils import timezone
import hashlib, datetime, random
from rest_framework import status
from django.http import HttpResponse
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from django.core import serializers
from django.views.generic.edit import UpdateView
from django.views.generic.base import TemplateView
from django.views.generic import ListView
from django.contrib.auth import logout
from django.contrib.auth import views
from django.db.models import get_model
from django.contrib.sites.models import Site
from django.core.paginator import Paginator, InvalidPage, EmptyPage

def contact_us(request):
    return render_to_response("/devconnect/contact-us.html", locals(), context_instance=RequestContext(request))

def map(request):
    return render_to_response("devconnect/portal.html", locals(), context_instance=RequestContext(request))

class parcelIndex(generic.ListView):
	queryset = Parcels.objects.all()
	#properties = crop.objects.all()
	template_name = "devconnect/land.html"
	paginate_by = 25
	
	def get(self, request, *args, **kwargs):
		parcel_list = Parcels.objects.filter(sale=True)
		var_get_search = request.GET.get('search_box')
		if var_get_search is not None:
			parcel_list = parcel_list.filter(Q(number__icontains=var_get_search)| Q(designated__icontains = var_get_search))
		paginator = Paginator(parcel_list, 25) # Show 25 contacts per page

		# Make sure page request is an int. If not, deliver first page.
		try:
			page = int(request.GET.get('page', '1'))
		except ValueError:
			page = 1

		# If page request (9999) is out of range, deliver last page of results.
		try:
			parcels = paginator.page(page)
		except (EmptyPage, InvalidPage):
			parcels = paginator.page(paginator.num_pages)
		return render(request, self.template_name, {'parcels': parcels})

class parcelDetail(generic.DetailView):
	model = Parcels
	template_name = "devconnect/lands.html"

def buyer(request):
    form = buyForm
    if request.method == 'POST':
        form = buyForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(commit=True)
            #return payment_portal(request)
            messages.success(request, 'Application Sent successfully')
            return HttpResponseRedirect(reverse("buyer"))
        else:
            print form.errors
    else:
        form = buyForm()
    images=Buy.objects.all()
    return render(request, 'devconnect/buyer.html', {'form': form,'images':images})
@login_required
def sell(request):
    form = saleForm
    if request.method == 'POST':
        form = saleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(commit=True)
            #return payment_portal(request)
            messages.success(request, 'Application Sent successfully')
            return HttpResponseRedirect(reverse("sell"))
        else:
            print form.errors
    else:
        form = saleForm()
    images=Sale.objects.all()
    return render(request, 'devconnect/sell.html', {'form': form,'images':images})

def register_user(request):
    args = {}
    args.update(csrf(request))
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        args['form'] = form
        if form.is_valid(): 
            form.save()  # save user to database if form is valid

            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            salt = hashlib.sha1(str(random.random())).hexdigest()[:5]            
            activation_key = hashlib.sha1(salt+email).hexdigest()            
            key_expires = datetime.datetime.today() + datetime.timedelta(2)

            #Get user by username
            user=User.objects.get(username=username)

            # Create and save user profile                                                                                                                                  
            new_profile = UserProfile(user=user, activation_key=activation_key, 
                key_expires=key_expires)
            new_profile.save()

            # Send email with activation key
            email_subject = 'Account confirmation'
            email_body = "Hey %s, thanks for signing up. To activate your account, click this link within 48hours http://127.0.0.1:8000/confirm/%s" % (username, activation_key)

            send_mail(email_subject, email_body, 'myemail@example.com',[email], fail_silently=False)
            messages.success(request, 'Account created successfully.Check your mail to activate!')
            return HttpResponseRedirect('/register/')
    else:
        args['form'] = RegistrationForm()

    return render_to_response('devconnect/register.html', args, context_instance=RequestContext(request))


def register_confirm(request, activation_key):
    if request.user.is_authenticated():
        HttpResponseRedirect('')

    user_profile = get_object_or_404(UserProfile, activation_key=activation_key)

    if user_profile.key_expires < timezone.now():
        return render_to_response('devconnect/confirm_expired.html')
    
    user = user_profile.user
    user.is_active = True
    user.save()
    return render_to_response('devconnect/confirm.html')
    messages.success(request, 'Confirmation successfull')

def user_login(request):
    args = {}
    args.update(csrf(request))
    if request.method == 'POST':
        
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            
            if user.is_active:

                if user.is_staff:
                    login(request, user)
                    return HttpResponseRedirect('/admin/')
                else:

                    login(request, user)
                    return HttpResponseRedirect('/')
                
            else:
                #return HttpResponseRedirect(reverse("login"))
                messages.error(request, "Error")
        else:
            
            messages.error(request, "Invalid username and password.Try again!")
            return render_to_response('devconnect/login.html', args, context_instance=RequestContext(request))

    
    else:
        
        return render(request, 'devconnect/login.html', {})

@login_required
def user_logout(request):
    logout(request)

    return HttpResponseRedirect('accounts/login/')

def change_password(request):
    template_response = views.password_change(request)
    # Do something with `template_response`
    return template_response
    messages.success(request, 'Password changed successfully!')

def contact(request):
    errors = []
    if request.method == 'POST':
        if not request.POST.get('subject', ''):
            errors.append('Enter a subject.')
        if not request.POST.get('message', ''):
            errors.append('Enter a message.')
        if request.POST.get('email') and '@' not in request.POST['email']:
            errors.append('Enter a valid e-mail address.')
        if not errors:
            send_mail(
                request.POST['subject'],
                request.POST['message'],
                request.POST.get('email', 'gegiskuct@gmail.com'),
                ['gegiskuct@gmail.com'], #email address where message is sent.
            )
            messages.success(request, 'Your message has been sent.Thank you for contacting us!') 
            
            return HttpResponseRedirect('/contacts/')
    return render(request, 'devconnect/contact-us.html',
        {'errors': errors}) 