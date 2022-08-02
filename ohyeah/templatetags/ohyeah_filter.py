from django import template
from datetime import datetime

register = template.Library()


@register.filter
def sub(value, arg):
    return value - arg

def next(value, arg):
    try:
        return value[int(arg)+1]
    except:
        return None
    
@register.filter
def convert_str_date(value):
    return datetime.strptime(value, '%Y-%m-%d').date()

@register.filter
def convert_str_month(value):
    return datetime.strptime(value, '%Y-%m').date()