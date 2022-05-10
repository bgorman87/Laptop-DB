from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django import forms
from .models import ContactUs

from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm

class UserLogin(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(UserLogin, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Username...'})
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password...'})

class CreateUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class' : 'form-control', "placeholder" : "Username...", "required" : "required", "disabled" : "disabled"})
        self.fields['email'].widget.attrs.update({'class' : 'form-control', "placeholder" : "Email...", "required" : "required", "disabled" : "disabled"})
        self.fields['password1'].widget.attrs.update({'class' : 'form-control', "placeholder" : "Password...", "required" : "required", "disabled" : "disabled"})
        self.fields['password2'].widget.attrs.update({'class' : 'form-control', "placeholder" : "Confirm Password...", "required" : "required", "disabled" : "disabled"})

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.password = make_password(self.cleaned_data["password1"])
        user.username = self.cleaned_data["username"]
        user.username = user.username.lower()
        if commit:
            user.save()
        return user

class UsernameVerification(forms.Form):
    username = forms.CharField(required=True, max_length=100)

    def __init__(self, *args, **kwargs):
        super(UsernameVerification, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class' : 'form-control', "name": "username", "placeholder" : "Username...", "required" : "required"})

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            return username
        else:
            raise forms.ValidationError("Username does not exist")

class UserPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(UserPasswordResetForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'label' : '', 'class' : 'form-control', "placeholder" : "Email...", "required" : "required"})

class UserPasswordChangeForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(UserPasswordChangeForm, self).__init__(*args, **kwargs)
        self.fields['new_password1'].widget.attrs.update({'class' : 'form-control', "placeholder" : "New Password...", "required" : "required"})
        self.fields['new_password2'].widget.attrs.update({'class' : 'form-control', "placeholder" : "Confirm New Password...", "required" : "required"})


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ('message',)
        widgets = {
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': '5', 'placeholder': 'Message...'})
        }
    
    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['message'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Message...'})

        
    def save(self, commit=True, message_type="general", created_by=None):
        contact = super(ContactForm, self).save(commit=False)
        contact.created_by = created_by
        contact.message_type = message_type
        if commit:
            contact.save()
        return contact
