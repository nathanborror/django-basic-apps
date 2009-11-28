from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import models
from django.utils import simplejson as json

Relationship = models.get_model('relationships', 'relationship')


@login_required
def follow(request, to_user_id, 
            template_name='relationships/relationship_add_confirm.html', 
            success_template_name='relationships/relationship_add_success.html', 
            mimetype='text/html'):
    """
    Allows a user to follow another user.
    
    Templates: ``relationships/relationship_add_confirm.html`` and ``relationships/relationship_add_success.html``
    Context:
        to_user
            User object
    """
    to_user = get_object_or_404(User, pk=to_user_id)
    from_user = request.user

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
            return HttpResponse(json.dumps(response), mimetype="application/json")
        else:
            template_name = success_template_name

    context = {'to_user': to_user}
    return render_to_response(template_name, context, context_instance=RequestContext(request), mimetype=mimetype)


@login_required
def unfollow(request, to_user_id, 
            template_name='relationships/relationship_delete_confirm.html', 
            success_template_name='relationships/relationship_delete_success.html', 
            mimetype='text/html'):
    """
    Allows a user to stop following another user.

    Templates: ``relationships/relationship_delete_confirm.html`` and ``relationships/relationship_delete_success.html``
    Context:
        to_user
            User object
    """
    to_user = get_object_or_404(User, pk=to_user_id)
    from_user = request.user

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
            return HttpResponse(json.dumps(response), mimetype="application/json")
        else:
            template_name = success_template_name

    context = {'to_user': to_user}
    return render_to_response(template_name, context, context_instance=RequestContext(request), mimetype=mimetype)


@login_required
def block(request, user_id, 
            template_name='relationships/block_confirm.html', 
            success_template_name='relationships/block_success.html', 
            mimetype='text/html'):
    """
    Allows a user to block another user.

    Templates: ``relationships/block_confirm.html`` and ``relationships/block_success.html``
    Context:
        user_to_block
            User object
    """
    user_to_block = get_object_or_404(User, pk=user_id)
    user = request.user

    if request.method == 'POST':
        relationship, created = Relationship.objects.get_or_create(to_user=user_to_block, from_user=user)
        relationship.is_blocked = True
        relationship.save()

        if request.is_ajax():
            response = {'success': 'Success'}
            return HttpResponse(json.dumps(response), mimetype="application/json")
        else:
            template_name = success_template_name

    context = {'user_to_block': user_to_block}
    return render_to_response(template_name, context, context_instance=RequestContext(request), mimetype=mimetype)


@login_required
def unblock(request, user_id, 
            template_name='relationships/block_delete_confirm.html', 
            success_template_name='relationships/block_delete_success.html', 
            mimetype='text/html'):
    """
    Allows a user to stop blocking another user.

    Templates: ``relationships/block_delete_confirm.html`` and ``relationships/block_delete_success.html``
    Context:
        user_to_block
            User object
    """
    user_to_block = get_object_or_404(User, pk=user_id)
    user = request.user

    if request.method == 'POST':
        relationship = get_object_or_404(Relationship, to_user=user_to_block, from_user=user, is_blocked=True)
        relationship.delete()

        if request.is_ajax():
            response = {'success': 'Success'}
            return HttpResponse(json.dumps(response), mimetype="application/json")
        else:
            template_name = success_template_name

    context = {'user_to_block': user_to_block}
    return render_to_response(template_name, context, context_instance=RequestContext(request), mimetype=mimetype)