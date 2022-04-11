# Users views.py

from django.forms import ValidationError
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm


from .forms import CreateUserForm, UsernameVerification, UserLogin
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from .decorators import allowed_users, unauthenticated_user
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator

from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

# Create your views here.
@login_required(login_url='login/')
@allowed_users(allowed_roles=['admin'])
def userPage (request, user_name=None):
    if user_name == None:
        user = request.user
        return redirect('profile-page', user_name=user.username)
    else:
        try:
            user = User.objects.get(username=user_name)
            if user.username.lower() == request.user.username.lower():
                msg = "You are viewing your own profile"
                return render(request, "base/user.html", {"passed_string": msg})
            else:
                msg = "You are viewing " + user.username + "'s profile"
                return render(request, 'base/user.html', {"passed_string": msg})
        except User.DoesNotExist:
            msg = f"Profile not found for {user_name}"
            return render(request, 'base/user.html', {"passed_string": msg})

    return render(request, 'base/user.html', {"user": user, "user_name": user_name})

@unauthenticated_user
def loginPage (request):
    form = UserLogin()
    if request.method == "POST":
        form = UserLogin(request.POST)
        username = request.POST.get('username')
        username = username.lower()
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        print(user)

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
            messages.error(request, "Username or password is incorrect")

    return render(request, 'base/login.html', {"form": form})

@login_required(login_url='login-page')
def logoutPage (request):
    logout(request)
    return redirect('home')

def naughty_user(request):
    return render(request, 'base/naughty.html', {})

@unauthenticated_user
def registerPage (request):
    
    form = CreateUserForm()

    if request.method == "POST":
        return redirect('naughty-page')
        
        form = CreateUserForm(request.POST)
        username = request.POST.get('username')
        username = username.lower()
        email = request.POST.get('email')

        if form.is_valid():
            try:
                _ = User.objects.get(username=username)
                messages.error(request, f"Username {username} already exists")
                return render(request, 'base/register.html', {"form": form})
            except:
                form.save()
                # user = User.objects.get(username=username)
                # user.username = username
                # user.save()
                # print(user)
                username = form.cleaned_data.get('username')
                username = username.lower()
                messages.success(request, "Account created successfully for " + username)
            return redirect('login-page')

        else:
            if username:
                try:
                    _ = User.objects.get(username=username)
                    messages.error(request, "Username already exists")
                    return render(request, 'base/register.html', {"form": form})
                except:
                    pass
            if email:
                try:
                    _ = User.objects.get(email=request.POST.get('email'))
                    messages.error(request, "Email already in system. Login instead")
                    return redirect('login-page')
                except:
                    pass
            
            if form.cleaned_data.get('password1') != form.cleaned_data.get('password2'):
                messages.error(request, "Passwords do not match")
                return render(request, 'base/register.html', {"form": form})

            messages.error(request, "Invalid form")


    return render(request, 'base/register.html', {"form": form})

def resetUsernameCheck(request):
    
    form = UsernameVerification()

    if request.method == "POST":
        for field in form:
            print("Field Error:", field.name,  field.errors)
        form = UsernameVerification(request.POST)
        if form.is_valid():
            print(form)
            username = form.clean_username()
            print(username)

            try:
                user = User.objects.get(username=username)
                
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                # return redirect('password_reset', uidb64=uidb64, token=token)
                return redirect('password_reset')
            except Exception as e:
                print(e)
                messages.error(request, "Username not found")
        else:
            messages.error(request, "Invalid form")
    
    return render(request, 'base/password-reset-username-check.html', {"form": form})


def passwordComplete(request):
    messages.success(request, "Password reset successful. Please login using your new credentials.")
    return redirect('login-page')