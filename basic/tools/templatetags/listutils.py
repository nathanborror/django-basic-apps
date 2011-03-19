from django.template import Library

register = Library()


@register.filter
def remaining(item_list, total):
    """
    Returns a null list of remaining items derived from the total. Usefull in
    situations where you want exactly ten items in an interface and you may only
    have eight items. 
    """
    list_length = len(item_list)
    expected_total = int(total)
    if list_length != expected_total:
        return range(0, expected_total-list_length)
    return ''


@register.filter
def pop_from_GET(obj, attr):
    """
    Returns GET parameters sans specified attribute.
    """
    if obj.get(attr, None):
        obj_copy = obj.copy()
        del obj_copy[attr]
        return '&%s' % obj_copy.urlencode()
    if not obj:
        return ''
    return '&%s' % obj.urlencode()


@register.filter
def empty_items(item_list, total):
    """
    Returns a list of null objects. Useful when you want to always show n
    results and you have a list of < n.
    """
    list_length = len(item_list)
    expected_total = int(total)
    if list_length != expected_total:
        return range(0, expected_total-list_length)
    return ''
