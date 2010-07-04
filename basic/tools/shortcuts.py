import os.path
import hashlib

from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http import HttpResponseRedirect


def get_image_path(instance, filename):
    """
    Converts an image filename to a hash.
    """
    name = hashlib.md5("%s" % instance.id).hexdigest()
    ext = os.path.splitext(filename)
    return os.path.join("%s/%s" % (instance._meta.app_label, instance._meta.module_name), '%s%s' % (name, ext[1]))


def render(request, *args, **kwargs):
    """
    Simple wrapper for render_to_response.
    """
    kwargs['context_instance'] = RequestContext(request)
    return render_to_response(*args, **kwargs)


def redirect(request, obj=None):
    """
    Simple wrapper for HttpResponseRedirect that checks the request for a
    'next' GET parameter then falls back to a given object or url string.
    """
    next = request.GET.get('next', None)
    redirect_url = '/'

    if next:
        redirect_url = next
    elif isinstance(obj, str):
        redirect_url = obj
    elif obj and hasattr(obj, 'get_absolute_url'):
        redirect_url = obj.get_absolute_url()
    return HttpResponseRedirect(redirect_url)