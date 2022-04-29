from django import template
from catalog.views import part_types

register = template.Library()

@register.filter(name='part_type') 
def part_type(part_type_id):
    return part_types[part_type_id]