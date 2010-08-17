from django.template import Library

register = Library()


@register.filter
def min_value(object_list, field):
    """
    Returns the min value given an object_list and a field.

    Example:
        {{ forecast|min:"high_temp" }}
    """
    value_list = [getattr(o, field, None) for o in object_list]
    return min(value_list)


@register.filter
def max_value(object_list, field):
    """
    Returns the max value given an object_list and a field.

    Example:
        {{ forecast|max:"high_temp" }}
    """
    value_list = [getattr(o, field, None) for o in object_list]
    return max(value_list)