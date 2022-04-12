from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField

CATEGORY_CHOICES = (
    ('KEYB', 'Keyboard'),
    ('BOTC', 'Bottom Cover'),
    ('PALR', 'Palm Rest'),
    ('LCDC', 'LCD Cover'),
    ('LCD', 'LCD'),
    ('CHAR', 'Charger'),
    ('BATT', 'Battery'),
    ('CHRP', 'Charging Port'),
    ('CPUF', 'CPU Fan'),
    ('LFTH', 'Left Hinge'),
    ('RGTH', 'Right Hinge'),
    ('SAT', 'SATA'),
    ('POR', 'Ports'),
    ('GRAC', 'Graphics Card'),
    ('RAM', 'RAM')
)

class Upload(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField()

class Serial_Number(models.Model):
    serial_number = models.CharField(max_length=200, unique=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.serial_number

class Laptop(models.Model):
    laptop_model = models.CharField(max_length=200, unique=True, null=True)
    manufacturer = models.CharField(max_length=200, null=True)
    series = models.CharField(max_length=200, null=True)
    serial_number = models.ManyToManyField(Serial_Number, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    country_id = CountryField(blank_label='-- Optional -- Select Country -- ', null=True, blank=True)
    image = models.ImageField(null=True, blank=True, default="default.png")
    
    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.laptop_model

class Part(models.Model):
    model = models.CharField(max_length=200, null=True, blank=True, unique=True)
    laptop_model = models.ManyToManyField(Laptop)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    country_id = CountryField(blank_label='-- Select Country --', null=True, blank=True)
    part_type = models.CharField(choices=CATEGORY_CHOICES, max_length=4, null=True, blank=True)
    image = models.ImageField(null=True, blank=True, default="default.png")

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.model