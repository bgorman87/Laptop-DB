from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField


class Laptop(models.Model):
    laptop_model = models.CharField(max_length=200, unique=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    country_id = CountryField(blank_label='(select country)', null=True)
    image = models.ImageField(null=True, blank=True, default="default.png")
    
    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.laptop_model


class Keyboard (models.Model):
    keyboard_model = models.CharField(max_length=200, null=True, blank=True, unique=True)
    laptop_model = models.ManyToManyField(Laptop)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    country_id = CountryField(blank_label='(select country)')
    image = models.ImageField(null=True, blank=True, default="default.png")
    
    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.keyboard_model

class Bottom_Cover (models.Model):
    bottom_cover_model = models.CharField(max_length=200, null=True, blank=True, unique=True)
    laptop_model = models.ManyToManyField(Laptop, blank=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(null=True, blank=True, default="default.png")

    class Meta:
        ordering = ['-updated', '-created']    

    def __str__(self):
        return self.bottom_cover_model

class Palm_Rest (models.Model):
    palm_rest_model = models.CharField(max_length=200, null=True, blank=True, unique=True)
    laptop_model = models.ManyToManyField(Laptop, blank=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(null=True, blank=True, default="default.png")
    
    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.palm_rest_model

class LCD_Cover (models.Model):
    lcd_cover_model = models.CharField(max_length=200, null=True, blank=True, unique=True)
    laptop_model = models.ManyToManyField(Laptop, blank=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(null=True, blank=True, default="default.png")
    
    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.lcd_cover_model

class LCD (models.Model):
    lcd_model = models.CharField(max_length=200, null=True, blank=True, unique=True)
    laptop_model = models.ManyToManyField(Laptop, blank=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(null=True, blank=True, default="default.png")
    
    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.lcd_model

class Charger (models.Model):
    charger_model = models.CharField(max_length=200, null=True, blank=True, unique=True)
    laptop_model = models.ManyToManyField(Laptop, blank=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(null=True, blank=True, default="default.png")
    
    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.charger_model

class Charging_Port (models.Model):
    charging_port_model = models.CharField(max_length=200, null=True, blank=True, unique=True)
    laptop_model = models.ManyToManyField(Laptop, blank=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(null=True, blank=True, default="default.png")
    
    class Meta:
            ordering = ['-updated', '-created']

    def __str__(self):
        return self.charging_port_model

class CPU_Fan (models.Model):
    cpu_fan_model = models.CharField(max_length=200, null=True, blank=True, unique=True)
    laptop_model = models.ManyToManyField(Laptop, blank=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(null=True, blank=True, default="default.png")
    
    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.cpu_fan_model

class Left_Hinge (models.Model):
    left_hinge_model = models.CharField(max_length=200, null=True, blank=True, unique=True)
    laptop_model = models.ManyToManyField(Laptop, blank=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(null=True, blank=True, default="default.png")
    
    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.left_hinge_model

class Right_Hinge (models.Model):
    right_hinge_model = models.CharField(max_length=200, null=True, blank=True, unique=True)
    laptop_model = models.ManyToManyField(Laptop, blank=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(null=True, blank=True, default="default.png")
    
    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.right_hinge_model


class SATA (models.Model):
    sata_model = models.CharField(max_length=200, null=True, blank=True, unique=True)
    laptop_model = models.ManyToManyField(Laptop, blank=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(null=True, blank=True, default="default.png")
    
    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.sata_model

class Ports (models.Model):
    ports_model = models.CharField(max_length=200, null=True, blank=True, unique=True)
    laptop_model = models.ManyToManyField(Laptop, blank=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(null=True, blank=True, default="default.png")
    
    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.ports_model

class Graphics_Card (models.Model):
    graphics_model = models.CharField(max_length=200, null=True, blank=True, unique=True)
    laptop_model = models.ManyToManyField(Laptop, blank=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(null=True, blank=True, default="default.png")
    
    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.graphics_model

class RAM (models.Model):
    ram_model = models.CharField(max_length=200, null=True, blank=True, unique=True)
    laptop_model = models.ManyToManyField(Laptop, blank=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(null=True, blank=True, default="default.png")
    
    class Meta:
        ordering = ['-updated', '-created']
    
    def __str__(self):
        return self.ram_model


class Battery(models.Model):
    battery_model = models.CharField(max_length=200, null=True, blank=True, unique=True)
    laptop_model = models.ManyToManyField(Laptop, blank=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(null=True, blank=True, default="default.png")
    
    class Meta:
        ordering = ['-updated', '-created']
    
    def __str__(self):
        return self.battery_model

