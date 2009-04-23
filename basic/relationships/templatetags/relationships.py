from django import template
from django.db import models

Relationship = models.get_model('relationships', 'relationship')
register = template.Library()


class GetRelationship(template.Node):
    def __init__(self, from_user, to_user, varname='relationship'):
        self.from_user = from_user
        self.to_user = to_user
        self.varname = varname
    
    def render(self, context):
        from_user = template.resolve_variable(self.from_user, context)
        to_user = template.resolve_variable(self.to_user, context)
        
        is_following = Relationship.objects.is_following(from_user, to_user)
        context[self.varname] = is_following
          
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