from django import template
from catalog.views import is_member
from users.models import ContactUs

register = template.Library() 

@register.filter(name="active_contact_submissions")
def active_contact_submissions(user, msg_type):
    if is_member(user, "admin"):
        count = ContactUs.objects.filter(message_type=msg_type, reviewed=False).count()
    else:
        count = 0
    return count