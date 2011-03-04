from django import template
from django.forms.widgets import Textarea
from datetime import datetime, timedelta

register = template.Library()

@register.filter(name='is_textarea')
def is_textarea(val):
    return isinstance(val, Textarea)

@register.filter(name='format_updated')
def format_updated(obj):
    dateval = obj.updated
    now = datetime.now()
    if now-timedelta(minutes=60) < dateval:
        return '%s minutes ago' % ((now-dateval).seconds / 60)
    if now-timedelta(days=1) < dateval:
        return '%s hours ago' % ((now-dateval).seconds / 3600)
    elif now-timedelta(days=7) < dateval:
        return '%s days ago' % ((now-dateval).days)
    elif now-timedelta(weeks=10) < dateval:
        return '%s weeks ago' % ((now-dateval).days / 7)
    else:
        return dateval.strftime('%m/%d/%y')

@register.filter(name='interviews_per_company_position')
def interviews_per_company_position(interview_set, company):
    # we need to filter by company
    return len(interview_set.filter(company=company))
