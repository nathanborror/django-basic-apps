import re

from django.template import Library, Template, Context
from django.template.defaultfilters import urlizetrunc
from django.utils.safestring import mark_safe

register = Library()


@register.filter
def twitterize(value):
    try:
        new_value = re.sub(r'(@)(\w+)', '\g<1><a href="/\g<2>/">\g<2></a>', value)
        return mark_safe(new_value)
    except:
        return value


@register.filter
def strip(value, arg):
    return value.strip(arg)


@register.filter
def smarty(value):
    from smartypants import smartyPants
    return value


@register.filter
def format_text(value):
    return twitterize(urlizetrunc(value, 30))


@register.filter
def format_field(field):
    t = Template("""
    <p class="ui-field{% if field.errors %} ui-error{% endif %}" {% if field.is_hidden %} style="display:none;"{% endif %}>
      {{ field.label_tag }}
      <span class="field">
        {% if field.errors %}<span class="ui-field-error">{{ field.errors|join:", " }}</span>{% endif %}
        {{ field }}
        {% if field.help_text %}<span class="ui-field-help">{{ field.help_text }}</span>{% endif %}
      </span>
    </p>
    """)
    return t.render(Context({'field': field}))


@register.filter
def format_fields(form):
    t = Template("""
    {% load stringutils %}
    {% for field in form %}
      {{ field|format_field }}
    {% endfor %}
    """)
    return t.render(Context({'form': form}))


@register.filter
def placeholder(field, text):
    return mark_safe(re.sub('<input ', '<input placeholder="%s" ' % text, field))
