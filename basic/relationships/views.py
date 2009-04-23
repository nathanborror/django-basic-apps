from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import models

Relationship = models.get_model('relationships', 'relationship')


@login_required
def follow(request, to_user_id, template_name='relationships/relationship_add_confirm.html', success_template_name='relationships/relationship_add_success.html', mimetype='text/html'):
    to_user = get_object_or_404(User, pk=to_user_id)
    from_user = request.user

    if request.is_ajax() or request.POST:
        relationship, created = Relationship.objects.get_or_create(from_user=from_user, to_user=to_user)

        if request.is_ajax():
            context = "{'success': 'Success', 'to_user_id': '%s'}" % (to_user.id)
            return HttpResponse(context, mimetype="application/json")
        else:
            template_name = success_template_name

    context = {'to_user': to_user}
    return render_to_response(template_name, context, context_instance=RequestContext(request), mimetype=mimetype)


@login_required
def stop_follow(request, to_user_id, template_name='relationships/relationship_delete_confirm.html', success_template_name='relationships/relationship_delete_success.html', mimetype='text/html'):
    to_user = get_object_or_404(User, pk=to_user_id)
    from_user = request.user
    
    if request.is_ajax() or request.POST:
        relationship = get_object_or_404(Relationship, to_user=to_user, from_user=from_user)
        relationship.delete()
        
        if request.is_ajax():
            context = "{'success': 'Success', 'to_user_id': '%s'}" % (to_user.id)
            return HttpResponse(context, mimetype="application/json")
        else:
            template_name = success_template_name
    
    context = {'to_user': to_user}
    return render_to_response(template_name, context, context_instance=RequestContext(request), mimetype=mimetype)