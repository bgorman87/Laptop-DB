from django.db import models, IntegrityError
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
    ('SATC', 'SATA Cable'),
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
    valid_extensions = ['.png', '.jpg', '.jpeg', '.gif'],
    valid = False
    if ext.lower() in valid_extensions:
        valid = True
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
    score = models.IntegerField(default=0)
    verified = models.BooleanField(default=False)    
    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.laptop_model

    def upvote(self, user):
        try:
            self.laptopvote_set.create(user=user, laptop=self, vote_type=True)
            self.score += 1
            self.save()
        except IntegrityError:
            vote = self.laptopvote_set.filter(user=user)
            if vote[0].vote_type == False:
                vote.update(vote_type=True)
                self.score += 2
                self.save()
                return "Downvote switched to upvote"
            elif vote[0].vote_type == True:
                self.score -= 1
                self.save()
                vote.delete()
                return "Removed upvote"
            else:
                return "You have already voted"
        return "Vote successful"


    def downvote(self, user):
        try:
            self.laptopvote_set.create(user=user, laptop=self, vote_type=False)
            self.score -= 1
            self.save()
        except IntegrityError:
            vote = self.laptopvote_set.filter(user=user)
            if vote[0].vote_type == True:
                vote.update(vote_type=False)
                self.score -= 2
                self.save()
                return "Upvote switched to downvote"
            elif vote[0].vote_type == False:
                self.score += 1
                self.save()
                vote.delete()
                return "Removed downvote"
            else:
                return "You have already voted"
        return "Vote successful"
    

class Part(models.Model):
    model = models.CharField(max_length=200, null=True, blank=True, unique=True)
    laptop_model = models.ManyToManyField(Laptop)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    country_id = CountryField(blank_label='-- Select Country --', null=True, blank=True)
    part_type = models.CharField(choices=CATEGORY_CHOICES, max_length=4, null=True, blank=True)
    image = models.FileField(null=True, blank=True, validators=[validate_image_file_extension])
    score = models.IntegerField(default=0)
    verified = models.BooleanField(default=False)
            
    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.model

    def upvote(self, user):
        try:
            self.partvote_set.create(user=user, part=self, vote_type=True)
            self.score += 1
            self.save()
        except IntegrityError:
            vote = self.partvote_set.filter(user=user)
            if vote[0].vote_type == False:
                vote.update(vote_type=True)
                self.score += 2
                self.save()
                return "Downvote switched to upvote"
            elif vote[0].vote_type == True:
                vote.update(vote_type=False)
                self.score -= 1
                self.save()
                vote.delete()
                return "Removed upvote"
            else:
                return "You have already voted"
        return "Upvote successful"

    def downvote(self, user):
        try:
            self.partvote_set.create(user=user, part=self, vote_type=False)
            self.score -= 1
            self.save()
        except IntegrityError:
            vote = self.partvote_set.filter(user=user)
            if vote[0].vote_type == True:
                vote.update(vote_type=False)
                self.score -= 2
                self.save()
                return "Upvote switched to downvote"
            elif vote[0].vote_type == False:
                self.score += 1
                self.save()
                vote.delete()
                return "Removed downvote"
            else:
                return "You have already voted"
        return "Downvote successful"

class PartVote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    part = models.ForeignKey(Part, on_delete=models.CASCADE)
    vote_type = models.BooleanField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'part')

class LaptopVote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    laptop = models.ForeignKey(Laptop, on_delete=models.CASCADE)
    vote_type = models.BooleanField()
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'laptop')

# Model to store part_model changes for admins to review and approve
class PartModelChange(models.Model):
    part = models.ForeignKey(Part, on_delete=models.CASCADE)
    old_model = models.CharField(max_length=200, null=True, blank=True)
    new_model = models.CharField(max_length=200, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='part_change_approved_by')
    approved_date = models.DateTimeField(null=True, blank=True)
    rejected_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='part_change_rejected_by')
    rejected_date = models.DateTimeField(null=True, blank=True)
    rejected_reason = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        ordering = ['-updated', '-created']

class LaptopModelChange(models.Model):
    laptop = models.ForeignKey(Laptop, on_delete=models.CASCADE)
    old_model = models.CharField(max_length=200, null=True, blank=True)
    new_model = models.CharField(max_length=200, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='laptop_change_approved_by')
    approved_date = models.DateTimeField(null=True, blank=True)
    rejected_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='laptop_change_rejected_by')
    rejected_date = models.DateTimeField(null=True, blank=True)
    rejected_reason = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        ordering = ['-updated', '-created']