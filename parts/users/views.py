# Users views.py

from django.forms import ValidationError
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def userPage (request, user_name=None):
    if user_name == None:
        user = request.user
        return redirect('profile-page', user_name=user.username)
    else:
        try:
            user = User.objects.get(username=user_name)
            if user.username == request.user.username:
                msg = "You are viewing your own profile"
                return render(request, "base/user.html", {"passed_string": msg})
            else:
                msg = "You are viewing " + user.username + "'s profile"
                return render(request, 'base/user.html', {"passed_string": msg})
        except User.DoesNotExist:
            msg = f"Profile not found for {user_name}"
            return render(request, 'base/user.html', {"passed_string": msg})

    return render(request, 'base/user.html', {"user": user, "user_name": user_name})

def loginPage (request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            try:
                next_page = request.POST.get('next')
                if next_page:
                    return redirect(next_page)
                else:
                    return redirect('home')
            except KeyError:
                return redirect('home')
            
        else:
            messages.info(request, "Username or password is incorrect")
    return render(request, 'base/login.html') 

@login_required(login_url='login-page')
def logoutPage (request):
    logout(request)
    return redirect('home')

def naughty_user(request):
    return render(request, 'base/naughty.html', {})

def registerPage (request):
    form = CreateUserForm()

    if request.method == "POST":
        return redirect('naughty-page')
        
        form = CreateUserForm(request.POST)
        username = request.POST.get('username')

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, "Account created successfully for " + username)
            return redirect('login-page')

        else:

            if User.objects.get(username=username):
                messages.error(request, "Username already exists")

            elif form.cleaned_data.get('password1') != form.cleaned_data.get('password2'):
                messages.error(request, "Passwords do not match")

            else:
                messages.error(request, "Invalid form")


    return render(request, 'base/register.html', {"form": form})