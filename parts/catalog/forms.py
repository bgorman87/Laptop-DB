from .models import *
from django.forms import ModelForm
from django.contrib.admin.widgets import AdminFileWidget
from django import forms


class LaptopForm(ModelForm):
    class Meta:
        model = Laptop
        exclude = ("created", "updated", "created_by",)
        widgets = {'serial_number': forms.TextInput(attrs={})}
    
    def __init__(self, *args, **kwargs):
        super(LaptopForm, self).__init__(*args, **kwargs)
        self.fields['laptop_model'].widget.attrs.update({'class' : 'form-control input-field', "placeholder" : "Required", "required" : "required"})
        self.fields['manufacturer'].widget.attrs.update({'class' : 'form-control input-field', "placeholder" : "Dell, Lenovo, HP, etc..."})
        self.fields['series'].widget.attrs.update({'class' : 'form-control input-field', "placeholder" : "XPS, Thinkpad, Envy, etc..."})
        self.fields['serial_number'].widget.attrs.update({'class' : 'form-control input-field', "placeholder" : "Optional"})
        

class PartForm(ModelForm):
    class Meta:
        model = Part
        fields = '__all__'
        exclude = ("created", "updated", "country_id", "created_by", "laptop_model",)
        widgets = {
            'image' : AdminFileWidget()
        }


        
class ModelChangeForm(forms.Form):
    current_model = forms.CharField(label="Current", max_length=100)
    suggested_model = forms.CharField(label="Suggested", max_length=100)

    def __init__(self, *args, **kwargs):
        super(ModelChangeForm, self).__init__(*args, **kwargs)
        self.fields['current_model'].widget.attrs.update({'class' : 'form-control', "disabled" : "disabled"})
        self.fields['suggested_model'].widget.attrs.update({'class' : 'form-control input-field', "placeholder" : "Required"})
