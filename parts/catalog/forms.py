from .models import *
from django.apps import apps
from django.forms import ModelForm, ChoiceField, Form, ClearableFileInput
from django.contrib.auth.models import User
from django.contrib.admin.widgets import AdminFileWidget
from django import forms


class LaptopForm(ModelForm):
    class Meta:
        model = Laptop
        exclude = ("created", "updated", "created_by",)
        widgets = {'serial_number': forms.TextInput(attrs={})}
    
    def __init__(self, *args, **kwargs):
        super(LaptopForm, self).__init__(*args, **kwargs)
        self.fields['laptop_model'].widget.attrs.update({'class' : 'form-control', "placeholder" : "Required", "required" : "required"})
        self.fields['manufacturer'].widget.attrs.update({'class' : 'form-control', "placeholder" : "Dell, Lenovo, HP, etc..."})
        self.fields['series'].widget.attrs.update({'class' : 'form-control', "placeholder" : "XPS, Thinkpad, Envy, etc..."})
        self.fields['serial_number'].widget.attrs.update({'class' : 'form-control', "placeholder" : "Optional"})
        

class PartForm(ModelForm):
    class Meta:
        model = Part
        fields = '__all__'
        exclude = ("created", "updated", "country_id", "created_by", "laptop_model",)
        widgets = {
            'image' : AdminFileWidget()
        }


        
