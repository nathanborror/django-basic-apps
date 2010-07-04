import datetime

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse

from basic.groups.models import Group, GroupMember


def membership_required(function=None):
    """
    Decorator for views that require user to be a member of a group, 
    redirecting to the group join page if necessary.
    """
    def decorator(request, *args, **kwargs):
        group = get_object_or_404(Group, slug=kwargs['slug'])
        if request.user.is_anonymous():
            return HttpResponseRedirect(reverse('django.contrib.auth.views.login'))
        if GroupMember.objects.is_member(group, request.user):
            return function(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('group_join', {'slug': group.slug}))
    return decorator


def ownership_required(function=None):
    """
    Decorator for views that require ownership status of a group.
    """
    def decorator(request, *args, **kwargs):
        group = get_object_or_404(Group, slug=kwargs['slug'])
        if request.user.is_anonymous():
            return HttpResponseRedirect(reverse('django.contrib.auth.views.login'))
        if GroupMember.objects.is_owner(group, request.user):
            return function(request, *args, **kwargs)
        else:
            raise Http404
    return decorator


def moderator_required(function=None):
    """
    Decorator for views that require moderator status of a group.
    """
    def decorator(request, *args, **kwargs):
        group = get_object_or_404(Group, slug=kwargs['slug'])
        if request.user.is_anonymous():
            return HttpResponseRedirect(reverse('django.contrib.auth.views.login'))
        if GroupMember.objects.is_moderator(group, request.user):
            return function(request, *args, **kwargs)
        else:
            raise Http404
    return decorator