from django import template
from django.forms.widgets import Textarea

register = template.Library()

@register.filter(name='is_textarea')
def is_textarea(val):
    return isinstance(val, Textarea)
