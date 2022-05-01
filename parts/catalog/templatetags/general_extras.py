from django import template
from catalog.views import part_types, is_member
from catalog.models import *

register = template.Library()

@register.filter(name='part_type') 
def part_type(part_type_id):
    return part_types[part_type_id]

@register.filter(name='part_change_requests')
def part_change_requests(user):
    notification_count = 0
    if is_member(user, 'mod'):
        notification_count += PartModelChange.objects.filter(approved_by=None, rejected_by=None).count()
    return notification_count

@register.filter(name='laptop_change_requests')
def laptop_change_requests(user):
    notification_count = 0
    if is_member(user, 'mod'):
        notification_count += LaptopModelChange.objects.filter(approved_by=None, rejected_by=None).count()
    return notification_count

@register.filter(name='notifications')
def notifications(user):
    notification_count = 0
    if is_member(user, 'mod'):
        notification_count += PartModelChange.objects.filter(approved_by=None, rejected_by=None).count()
        notification_count += LaptopModelChange.objects.filter(approved_by=None, rejected_by=None).count()
    return notification_count