from django.template import Library
from django.template.defaultfilters import lower
from django.utils.safestring import mark_safe

register = Library()


@register.filter
def is_content_type(obj, arg):
    try:
        ct = lower(obj._meta.object_name)
        return ct == arg
    except AttributeError:
        return ''


@register.filter
def app_label(obj):
    """
    Returns an objects app label.
    """
    try:
        return lower(obj._meta.object_name)
    except AttributeError:
        return ''


@register.filter
def round(obj):
    """
    Returns a number rounded.
    """
    try:
        return round(obj)
    except (ValueError,TypeError):
        return ''


@register.filter
def is_string(obj):
    return isinstance(obj, str)


@register.filter
def is_number(obj):
    return isinstance(obj, int)


@register.filter
def is_on(obj1, obj2):
    """
    Shortcut to render an 'on' class.
    """
    if obj1 == obj2:
        return mark_safe(' class="on"')
    return ''
