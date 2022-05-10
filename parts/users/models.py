#Users models.py

from django.db import models
from django.contrib.auth.models import User

class ContactUs(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(blank=False)
    message_type = models.CharField(max_length=20, choices=(("general", "General"), ("bug", "Bug"), ("suggestion", "Suggestion")))
    reviewed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def snippet(self):
        return self.message[:50] + "..."