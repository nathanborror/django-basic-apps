from django import template


def parse_ttag(token, required_tags):
    """
    A function to parse a template tag.
    Pass in the token to parse, and a list of keywords to look for.
    It sets the name of the tag to 'tag_name' in the hash returned.

    >>> from test_utils.templatetags.utils import parse_ttag
    >>> parse_ttag('super_cool_tag for my_object as bob', ['as'])
    {'tag_name': u'super_cool_tag', u'as': u'bob'}
    >>> parse_ttag('super_cool_tag for my_object as bob', ['as', 'for'])
    {'tag_name': u'super_cool_tag', u'as': u'bob', u'for': u'my_object'}

    Author:     Eric Holscher
    URL:        http://github.com/ericholscher/
    """

    if isinstance(token, template.Token):
        bits = token.split_contents()
    else:
        bits = token.split(' ')
    tags = {'tag_name': bits.pop(0)}
    for index, bit in enumerate(bits):
        bit = bit.strip()
        if bit in required_tags:
            if len(bits) != index-1:
                tags[bit.strip()] = bits[index+1]
    return tags