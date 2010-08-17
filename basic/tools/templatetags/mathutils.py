from django import template
from django.template import Library
from django.template import TemplateSyntaxError, VariableDoesNotExist

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


class RatioNode(template.Node):
    def __init__(self, val_expr, min_expr, max_expr, max_width):
        self.val_expr = val_expr
        self.min_expr = min_expr
        self.max_expr = max_expr
        self.max_width = max_width

    def render(self, context):
        try:
            value = self.val_expr.resolve(context)
            minvalue = self.min_expr.resolve(context)
            maxvalue = self.max_expr.resolve(context)
            max_width = int(self.max_width.resolve(context))
        except VariableDoesNotExist:
            return ''
        except ValueError:
            raise TemplateSyntaxError("widthratio final argument must be an number")
        try:
            value = float(max(value, minvalue))
            maxvalue = float(maxvalue)
            minvalue = float(minvalue)
            #ratio = (value / maxvalue) * max_width
            ratio = (value - minvalue)/(maxvalue - minvalue)*max_width
        except (ValueError, ZeroDivisionError):
            return ''
        return str(int(round(ratio)))


@register.tag
def ratio(parser, token):
    """
    For creating bar charts and such, this tag calculates the ratio of a given
    value to a maximum value, and then applies that ratio to a constant.

    For example::

        {% ratio this_value min_value max_value 100 %}
        {% ratio 55 40 90 100 %}
    """
    bits = token.contents.split()
    if len(bits) != 5:
        raise TemplateSyntaxError("widthratio takes three arguments")
    tag, this_value_expr, min_value_expr, max_value_expr, max_width = bits

    return RatioNode(parser.compile_filter(this_value_expr),
                          parser.compile_filter(min_value_expr),
                          parser.compile_filter(max_value_expr),
                          parser.compile_filter(max_width))
