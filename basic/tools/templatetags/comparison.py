from django.template import Library
from django.template.defaultfilters import lower

register = Library()

@register.filter
def gt(value, arg):
    "Returns a boolean of whether the value is greater than the argument"
    try:
        return float(value) > float(arg)
    except (ValueError,TypeError):
        return ""

@register.filter
def lt(value, arg):
    "Returns a boolean of whether the value is less than the argument"
    try:
        return float(value) < float(arg)
    except (ValueError,TypeError):
        return ""

@register.filter
def gte(value, arg):
    "Returns a boolean of whether the value is greater than or equal to the argument"
    try:
        return float(value) >= float(arg)
    except (ValueError,TypeError):
        return ""

@register.filter
def lte(value, arg):
    "Returns a boolean of whether the value is less than or equal to the argument"
    try:
        return float(value) <= float(arg)
    except (ValueError,TypeError):
        return ""

@register.filter
def is_content_type(obj, arg):
    try:
        ct = lower(obj._meta.object_name)
        return ct == arg
    except AttributeError:
        return ""

@register.filter
def is_equal(obj, arg):
    "Returns a boolean of whether the value is equal to the argument"
    return obj == arg

@register.filter
def round(obj):
    "Returns a number rounded."
    try:
        return round(obj)
    except (ValueError,TypeError):
        return ""

@register.filter
def has(obj, arg):
    "Returns a boolean of whether the value is in a list of values or a string"
    try:
        if arg in obj:
            return True
    except TypeError:
        return ""
    return False


@register.filter
def is_string(obj):
    return isinstance(obj, str)


@register.filter
def is_number(obj):
    return isinstance(obj, int)


@register.filter
def get_vars(obj):
    getvars = obj.copy()
    if 'page' in obj:
        del getvars['page']
    if len(getvars.keys()) > 0:
        return "&%s" % getvars.urlencode()
    else:
        return ''