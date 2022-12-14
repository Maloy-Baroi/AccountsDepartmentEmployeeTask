from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.
from django.urls import reverse

from App_auth.forms import SignUpForm
from App_auth.models import User


def is_boss(user):
    return user.groups.filter(name="Boss").exists()


def is_employee(user):
    return user.groups.filter(name="Employee").exists()


def signup_view(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            my_admin_group = Group.objects.get_or_create(name='Employee')
            my_admin_group[0].user_set.add(user)
            return HttpResponseRedirect(reverse('App_auth:login-page'))
    content = {
        'form': form,
    }
    return render(request, 'App_auth/signup_page.html', context=content)


def login_view(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user_email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=user_email, password=password)
            if user:
                login(request, user)
                if is_boss(user):
                    return HttpResponseRedirect(reverse('App_main:boss-dashboard'))
                elif is_employee(user):
                    return HttpResponseRedirect(reverse('App_main:employee-dashboard'))
    content = {
        'form': form,
    }
    return render(request, 'App_auth/login_view.html', context=content)


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('App_auth:login'))
