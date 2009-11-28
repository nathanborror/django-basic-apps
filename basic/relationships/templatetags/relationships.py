from django import template
from django.db import models

Relationship = models.get_model('relationships', 'relationship')
register = template.Library()


# Expose RelationshipManager functionality as template filters.

@register.filter
def blockers(user):
    """Returns list of people blocking user."""
    try:
        return Relationship.objects.get_blockers_for_user(user)
    except AttributeError:
        return []

@register.filter
def friends(user):
    """Returns people user is following sans people blocking user."""
    try:
        return Relationship.objects.get_friends_for_user(user)
    except AttributeError:
        return []

@register.filter
def followers(user):
    """Returns people following user."""
    try:
        return Relationship.objects.get_followers_for_user(user)
    except AttributeError:
        pass

@register.filter
def fans(user):
    """Returns people following user but user isn't following."""
    try:
        return Relationship.objects.get_fans_for_user(user)
    except AttributeError:
        pass

# Comparing two users.

@register.filter
def follows(from_user, to_user):
    """Returns ``True`` if the first user follows the second, ``False`` otherwise.  Example: {% if user|follows:person %}{% endif %}"""
    try:
        relationship = Relationship.objects.get_relationship(from_user, to_user)
        if relationship and not relationship.is_blocked:
            return True
        else:
            return False
    except AttributeError:
        return False

@register.filter
def get_relationship(from_user, to_user):
    """Get relationship between two users."""
    try:
        return Relationship.objects.get_relationship(from_user, to_user)
    except AttributeError:
        return None

# get_relationship templatetag.

class GetRelationship(template.Node):
    def __init__(self, from_user, to_user, varname='relationship'):
        self.from_user = from_user
        self.to_user = to_user
        self.varname = varname

    def render(self, context):
        from_user = template.resolve_variable(self.from_user, context)
        to_user = template.resolve_variable(self.to_user, context)

        relationship = Relationship.objects.get_relationship(from_user, to_user)
        context[self.varname] = relationship

        return ''

def do_get_relationship(parser, token):
    """
    Get relationship between two users.

    Example:
        {% get_relationship from_user to_user as relationship %}
    """
    bits = token.contents.split()
    if len(bits) == 3:
        return GetRelationship(bits[1], bits[2])
    if len(bits) == 5:
        return GetRelationship(bits[1], bits[2], bits[4])
    if len(bits) == 4:
        raise template.TemplateSyntaxError, "The tag '%s' needs an 'as' as its third argument." % bits[0]
    if len(bits) < 3:
        raise template.TemplateSyntaxError, "The tag '%s' takes two arguments" % bits[0]

register.tag('get_relationship', do_get_relationship)
