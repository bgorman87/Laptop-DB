# Users views.py


from django.shortcuts import render, redirect
from .forms import *
from .models import ContactUs
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .decorators import unauthenticated_user
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from verify_email.email_handler import send_verification_email
from catalog.views import is_member
from datetime import timedelta
from django.utils import timezone

# Create your views here.
@login_required(login_url='login/')
def userPage (request, user_name=None):

    if not is_member(request.user, "admin"):
        return render(request, 'base/user-page-notice.html', {})
    
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
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')

        if form.is_valid():
            
            try:
                username = form.cleaned_data['username']
                _ = User.objects.get(username=username)
                messages.error(request, f"Username {username} already exists")
                return render(request, 'base/register.html', {"form": form})
            except:
                inactive_user = send_verification_email(request, form)
                # user = User.objects.get(username=username)
                # user.username = username
                # user.save()
                # print(user)
                messages.success(request, "Please check your email for verification to login")
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
        
        form = UsernameVerification(request.POST)
        if form.is_valid():

            username = form.clean_username()


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


    # form page to be used for both issues and suggestions. Form results emailed to the admin.
@login_required(login_url='login-page')
def contact_admin(request):
    
    try:
        last_submission_time = ContactUs.objects.filter(created_by=request.user).order_by('-created_at').first().created_at
        allowed_time = timezone.now() - timedelta(seconds=30)
        if last_submission_time > allowed_time:
            difference = last_submission_time - allowed_time
            if difference > timedelta(seconds=1):
                msg = f"You have already submitted a message. Please wait {str(difference).split(':')[-1].split('.')[0]} more seconds before submitting another."
            else:
                msg = f"You have already submitted a message. Please wait {str(difference).split(':')[-1].split('.')[0]} more second before submitting another."

            messages.error(request, msg)
            return redirect('home')
    except:
        pass


    if request.method == "POST":

        form = ContactForm(request.POST)

        message = request.POST.get('message')
        if len(message) < 10:
            messages.error(request, "Message must be at least 10 characters")
            return render(request, "base/contact-admin.html", {'form': form})


        msg_type = request.POST.get("msg_type")
        if not msg_type:
            messages.error(request, "Please select a type of message to send")
            return render(request, "base/contact-admin.html", {'form': form})


        user = request.user

        form.created_by = user
        if form.is_valid():
            try:
                subject = msg_type.capitalize() + " - LaptopDB Contact Us Form Message"
                message = "From User: " + user.username + "\n" + "Name: " + user.first_name + " " + user.last_name + "\n" + "User Email: " + user.email + "\n" + "Joined: " + str(user.date_joined) + "\n\n" + form.cleaned_data['message']
                sender = settings.FROM_EMAIL
                recipients = [settings.FROM_EMAIL]
                send_mail(subject, message, sender, recipients)
                messages.success(request, f"{msg_type.capitalize()} submission successful.")
            except Exception as e:
                print(e)
                messages.error(request, f"Error sending message.")
                return render(request, "base/contact-admin.html", {'form': form})
            
            try:
                form.save(message_type=msg_type, created_by=user)
            except Exception as e:
                print(e)
            return redirect('home')
        else:
            print(form.errors)
            messages.error(request, f"Invalid Form.")
            return render(request, "base/contact-admin.html", {'form': form})
        
    else:
        form = ContactForm()
    return render(request, "base/contact-admin.html", {'form': form})

def active_contact_submissions(request, msg_type):
    
    if not is_member(request.user, "admin"):
        return redirect('home')

    title = msg_type.capitalize()

    submissions = ContactUs.objects.filter(message_type=msg_type).filter(reviewed=False)

    return render(request, "base/active-contact-submissions.html", {'submissions': submissions, 'title': title})

def active_contact_review(request, contact_id):
    if not is_member(request.user, "admin"):
        return redirect('home')
    
    submission = ContactUs.objects.get(id=contact_id)

    if request.method == "POST":
        if request.POST.get('option') == "reviewed":
            submission.reviewed = True
            submission.save()
            messages.success(request, "Submission marked as reviewed.")
            return redirect('active-contact-submissions', msg_type=submission.message_type)
        else:
            submission.reviewed = False
            submission.save()
            return redirect('active-contact-submissions', msg_type=submission.message_type)


    return render(request, "base/active-contact-review.html", {'submission': submission})
