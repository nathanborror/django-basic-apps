import json

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, InvalidPage
from django.db import models
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.template.loader import render_to_string

Relationship = models.get_model('relationships', 'relationship')


FOLLOWING_PER_PAGE = getattr(settings, 'RELATIONSHIPS_FOLLOWING_PER_PAGE', 20)
FOLLOWERS_PER_PAGE = getattr(settings, 'RELATIONSHIPS_FOLLOWERS_PER_PAGE', 20)


def following(request, username,
              template_name='relationships/relationship_following.html',
              flat=True):
    from_user = get_object_or_404(User, username=username)
    following_ids = Relationship.objects.get_friends_for_user(from_user, flat=flat)
    following = User.objects.filter(pk__in=following_ids)
    paginator = Paginator(following, FOLLOWING_PER_PAGE)

    try:
        page = paginator.page(int(request.GET.get('page', 1)))
    except InvalidPage:
        raise Http404("No such page.")

    return render_to_response(template_name, {
        'person': from_user,
        'page': page,
        'paginator': paginator,
    }, context_instance=RequestContext(request))


def followers(request, username,
              template_name='relationships/relationship_followers.html',
              flat=True):
    to_user = get_object_or_404(User, username=username)
    followers_ids = Relationship.objects.get_followers_for_user(to_user, flat=True)
    followers = User.objects.filter(pk__in=followers_ids)
    paginator = Paginator(followers, FOLLOWERS_PER_PAGE)

    try:
        page = paginator.page(int(request.GET.get('page', 1)))
    except InvalidPage:
        raise Http404("No such page.")

    return render_to_response(template_name, {
        'person': to_user,
        'page': page,
        'paginator': paginator,
    }, context_instance=RequestContext(request))


@login_required
def follow(request, username,
            template_name='relationships/relationship_add_confirm.html', 
            success_template_name='relationships/relationship_add_success.html', 
            content_type='text/html'):
    """
    Allows a user to follow another user.
    
    Templates: ``relationships/relationship_add_confirm.html`` and ``relationships/relationship_add_success.html``
    Context:
        to_user
            User object
    """
    to_user = get_object_or_404(User, username=username)
    from_user = request.user
    next = request.GET.get('next', None)

    if request.method == 'POST':
        relationship, created = Relationship.objects.get_or_create(from_user=from_user, to_user=to_user)

        if request.is_ajax():
            response = {
                'success': 'Success',
                'to_user': {
                    'username': to_user.username,
                    'user_id': to_user.pk
                },
                'from_user': {
                    'username': from_user.username,
                    'user_id': from_user.pk
                }
            }
            return HttpResponse(json.dumps(response), content_type="application/json")
        if next:
            return HttpResponseRedirect(next)
        template_name = success_template_name

    context = {
        'to_user': to_user,
        'next': next
    }
    return render_to_response(template_name, context, context_instance=RequestContext(request), content_type=content_type)


@login_required
def unfollow(request, username,
            template_name='relationships/relationship_delete_confirm.html', 
            success_template_name='relationships/relationship_delete_success.html', 
            content_type='text/html'):
    """
    Allows a user to stop following another user.

    Templates: ``relationships/relationship_delete_confirm.html`` and ``relationships/relationship_delete_success.html``
    Context:
        to_user
            User object
    """
    to_user = get_object_or_404(User, username=username)
    from_user = request.user
    next = request.GET.get('next', None)

    if request.method == 'POST':
        relationship = get_object_or_404(Relationship, to_user=to_user, from_user=from_user)
        relationship.delete()

        if request.is_ajax():
            response = {
                'success': 'Success',
                'to_user': {
                    'username': to_user.username,
                    'user_id': to_user.pk
                },
                'from_user': {
                    'username': from_user.username,
                    'user_id': from_user.pk
                }
            }
            return HttpResponse(json.dumps(response), content_type="application/json")
        if next:
            return HttpResponseRedirect(next)
        template_name = success_template_name

    context = {
        'to_user': to_user,
        'next': next
    }
    return render_to_response(template_name, context, context_instance=RequestContext(request), content_type=content_type)


@login_required
def block(request, username,
            template_name='relationships/block_confirm.html', 
            success_template_name='relationships/block_success.html', 
            content_type='text/html'):
    """
    Allows a user to block another user.

    Templates: ``relationships/block_confirm.html`` and ``relationships/block_success.html``
    Context:
        user_to_block
            User object
    """
    user_to_block = get_object_or_404(User, username=username)
    user = request.user
    next = request.GET.get('next', None)

    if request.method == 'POST':
        relationship, created = Relationship.objects.get_or_create(to_user=user_to_block, from_user=user)
        relationship.is_blocked = True
        relationship.save()

        if request.is_ajax():
            response = {'success': 'Success'}
            return HttpResponse(json.dumps(response), content_type="application/json")
        if next:
            return HttpResponseRedirect(next)
        template_name = success_template_name

    context = {
        'user_to_block': user_to_block,
        'next': next
    }
    return render_to_response(template_name, context, context_instance=RequestContext(request), content_type=content_type)


@login_required
def unblock(request, username,
            template_name='relationships/block_delete_confirm.html', 
            success_template_name='relationships/block_delete_success.html', 
            content_type='text/html'):
    """
    Allows a user to stop blocking another user.

    Templates: ``relationships/block_delete_confirm.html`` and ``relationships/block_delete_success.html``
    Context:
        user_to_block
            User object
    """
    user_to_block = get_object_or_404(User, username=username)
    user = request.user

    if request.method == 'POST':
        relationship = get_object_or_404(Relationship, to_user=user_to_block, from_user=user, is_blocked=True)
        relationship.delete()

        if request.is_ajax():
            response = {'success': 'Success'}
            return HttpResponse(json.dumps(response), content_type="application/json")
        else:
            template_name = success_template_name

    context = {'user_to_block': user_to_block}
    return render_to_response(template_name, context, context_instance=RequestContext(request), content_type=content_type)
