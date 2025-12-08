from django import template
from taxi.models import Driver

register = template.Library()


@register.filter
def is_driver(user):
    return isinstance(user, Driver)
