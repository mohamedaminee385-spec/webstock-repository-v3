from django import template
from django.utils.dateformat import format
from datetime import datetime, date

register = template.Library()

@register.filter(name="updated")
def updated(value, format_string="M d, Y H:i"):
    """
    Formats a datetime/date object using the provided format string.
    If value is None or invalid, returns an empty string.
    """
    if not value:
        return ""

    if isinstance(value, (datetime, date)):
        return format(value, format_string)

    return value