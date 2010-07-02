import re

from django.template import Library, Template, Context
from django.contrib.markup.templatetags.markup import markdown
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
    return twitterize(urlizetrunc(markdown(value), 30))


@register.filter
def format_field(field):
    t = Template("""
    <p>
      {{ field.label_tag }}
      <span class="field">
        {{ field }}
        {% if field.help_text %}<span class="help_text">{{ field.help_text }}</span>{% endif %}
        {% if field.errors %}<span class="errors">{{ field.errors|join:", " }}</span>{% endif %}
      </span>
    </p>
    """)
    return t.render(Context({'field': field}))