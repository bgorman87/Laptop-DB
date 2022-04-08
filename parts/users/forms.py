from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django import forms

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
        if commit:
            user.save()
        return user