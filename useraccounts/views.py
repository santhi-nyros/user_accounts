from django.shortcuts import render
from django.shortcuts import get_object_or_404, render, redirect, render_to_response
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.models import User, Group
from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage

from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template import loader
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models.query_utils import Q
from django.core.urlresolvers import reverse

# Import the built-in password reset view and password reset confirmation view.
from django.contrib.auth.views import password_reset, password_reset_confirm

from .forms import *
from .models import UserProfle
# Create your views here.


#User registration
def regisration(request):
    form = RegistrationForm()
    if request.method == 'POST': # Post method
        username = request.POST['username']
        f_name = request.POST['first_name']
        l_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        address = request.POST['address']
        try :
            # checking for new user or existed user
            user = User.objects.get(email=email)
            status = 'User alredy existed with this mails.Please go with login.'
        except User.DoesNotExist :
            # if new user save the details in database
            user = User()
            user.username = username
            user.first_name = f_name
            user.last_name = l_name
            user.email = email
            user.set_password(password)
            user.save()
            uprof = UserProfle()
            uprof.user = user
            uprof.address = address
            uprof.save()
            status = 'User succesfully registrated, please go with login page.'
        return render(request,'registration.html',{"form":form,'status':status})
    # if Get method
    return render(request,'registration.html',{"form":form})



#User Login
def login(request):
    form = LoginForm()
    if request.method =='POST':# POST method
        email = request.POST['email']
        password = request.POST['password']
        try:
            #if user is existed or not
            user = User.objects.get(email=email)
            user = auth.authenticate(username=user.username, password=password)
            if user is not None:
                if user.is_active:
                    auth.login(request, user) # login the user
                    return HttpResponseRedirect('/')
            else:
                status = "The email or password you have entered is invalid!"
        except User.DoesNotExist :
            status = "User does not existed with this mail, please go with registration page."
        return render(request,'login.html',{"form":form,"status":status})
    # Get method
    return render(request,'login.html',{"form":form})


# Logout
@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')


# Updating user details
@login_required
def updateProfile(request):
    user = User.objects.get(email = request.user.email)
    u_profile = UserProfle.objects.get(user = user)
    form = EditForm(initial={'username': user, 'first_name':user.first_name,'last_name':user.last_name,'address':u_profile.address})
    if request.method == 'POST':
        user.username = request.POST['username']
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.save()
        u_profile.address = request.POST['address']
        u_profile.save()
        return HttpResponseRedirect('/accounts/update/')
    return render(request,'update.html',{"form":form})


# authenticated user password reset
@login_required
def password_reset(request):
    form = PasswordResetForm()
    if request.method == 'POST':
        if (request.POST['password'] == request.POST['password_confirm']):
            user = User.objects.get(email = request.user.email)
            user.set_password(request.POST['password'])
            user.save()
            return HttpResponseRedirect("/accounts/login/")
        return render(request,'reset_password.html',{"form":form ,'status':'Password mismatched,please try again.'})
    return render(request,'reset_password.html',{"form":form})

