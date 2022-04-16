from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django.core.exceptions import ValidationError
from django.core.validators import validate_image_file_extension

CATEGORY_CHOICES = (
    ('KEYB', 'Keyboard'),
    ('BOTC', 'Bottom Cover'),
    ('PALR', 'Palm Rest'),
    ('LCDC', 'LCD Cover'),
    ('LCD', 'LCD'),
    ('LCDB', 'LCD Bezel'),
    ('LCDT', 'LCD Touch Assembly'),
    ('TRA', 'Trackpad'),
    ('SPE', 'Speakers'),
    ('MIC', 'Microphone'),
    ('CAM', 'Camera'),
    ('POW', 'Power Button'),
    ('HEAT', 'Heatsink'),
    ('CDD', 'CD Drive'),
    ('WIFI', 'Wi-Fi Adapter'),
    ('MOTH', 'Motherboard'),
    ('WIFA', 'Wi-Fi Antenna'),
    ('DICA', 'Display Cable'),
    ('HDDC', 'Hard Drive Caddy'),
    ('TPFC', 'Trackpad Flex Cable'),
    ('PBFC', 'Power Button Flex Cable'),
    ('SB01', 'Sub Board 1'),
    ('SB02', 'Sub Board 2'),
    ('SB03', 'Sub Board 3'),
    ('SBFC', 'Sub Board Flex Cable'),
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

# class Upload(models.Model):
#     uploaded_at = models.DateTimeField(auto_now_add=True)
#     file = models.FileField()

def validate_file_extension(value):
    import os
    ext = os.path.splitext(value.name)[-1]
    print(ext)
    valid_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.JPG', '.PNG', '.JPEG', '.GIF'],
    valid = False
    for extension in valid_extensions:
        if extension == ext:
            valid = True
            break    
    if not valid:
        raise ValidationError(u'File not supported!')


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
    manufacturer = models.CharField(max_length=200, null=True, blank=True)
    series = models.CharField(max_length=200, null=True, blank=True)
    serial_number = models.ManyToManyField(Serial_Number, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    country_id = CountryField(blank_label='-- Optional -- Select Country -- ', null=True, blank=True)
    image = models.FileField(null=True, blank=True, validators=[validate_image_file_extension])
    
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
    image = models.FileField(null=True, blank=True, validators=[validate_image_file_extension])

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.model