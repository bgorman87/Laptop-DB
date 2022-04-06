from .models import *
from django.apps import apps
from django.forms import ModelForm, ChoiceField, Form, ClearableFileInput
from django.contrib.auth.models import User
from django.contrib.admin.widgets import AdminFileWidget


class LaptopForm(ModelForm):
    class Meta:
        model = Laptop
        exclude = ("created", "updated", "created_by",)
        # widgets = {'country': CountrySelectWidget()}
        

class PartForm(ModelForm):
    class Meta:
        model = Part
        fields = '__all__'
        exclude = ("created", "updated", "country_id", "created_by", "laptop_model",)
        widgets = {
            'image' : AdminFileWidget()
        }
        
