from django.shortcuts import get_object_or_404, render_to_response
from django.http import Http404, HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.contenttypes.models import ContentType

from basic.messages.models import Message, TO_STATUS_READ, TO_STATUS_DELETED, FROM_STATUS_DELETED
from basic.messages.forms import MessageForm
from basic.tools.baseconv import base62

@login_required
def message_list(request, mailbox=None, template_name='messages/message_list.html'):
    """
    Returns a list of user messages.

    Template:: ``messages/message_list.html``
    Context:
        message_list
            List of Message objects
        mailbox
            String representing the current 'mailbox'
    """
    if mailbox == 'sent':
        message_list = Message.objects.sent(request.user)
    elif mailbox == 'inbox':
        message_list = Message.objects.new(request.user)
    elif mailbox == 'trash':
        message_list = Message.objects.trash(request.user)
    else:
        message_list = Message.objects.archive(request.user)

    return render_to_response(template_name, {
        'message_list': message_list,
        'mailbox': mailbox or 'archive'
    }, context_instance=RequestContext(request))


@login_required
def message_create(request, content_type_id=None, object_id=None, 
                    template_name='messages/message_form.html'):
    """
    Handles a new message and displays a form.

    Template:: ``messages/message_form.html``
    Context:
        form
            MessageForm object
    """
    if request.GET.get('to', None):
        to_user = get_object_or_404(User, username=request.GET['to'])
    else:
        to_user = None
    
    if content_type_id and object_id:
        content_type = ContentType.objects.get(pk=base62.to_decimal(content_type_id))
        Model = content_type.model_class()
        try:
            related_object = Model.objects.get(pk=base62.to_decimal(object_id))
        except ObjectDoesNotExist:
            raise Http404, "The object ID was invalid."
    else:
        related_object = None
    
    form = MessageForm(request.POST or None, initial={'to_user': to_user})
    if form.is_valid():
        message = form.save(commit=False)
        if related_object:
            message.object = related_object
        message.from_user = request.user
        message = form.save()
        return HttpResponseRedirect(reverse('messages:messages'))
    return render_to_response(template_name, {
        'form': form,
        'to_user': to_user,
        'related_object': related_object
    }, context_instance=RequestContext(request))


def message_reply(request, object_id, template_name='messages/message_form.html'):
    """
    Handles a reply to a specific message.
    """
    original_message = get_object_or_404(Message, pk=object_id)
    form = MessageForm(request.POST or None, initial={'to_user': original_message.from_user})
    if form.is_valid():
        message = form.save(commit=False)
        message.object = original_message
        message.from_user = request.user
        message = form.save()
        return HttpResponseRedirect(reverse('messages:messages'))
    return render_to_response(template_name, {
        'form': form,
        'message': original_message
    }, context_instance=RequestContext(request))


@login_required
def message_remove(request, object_id, template_name='messages/message_remove_confirm.html'):
    """
    Remove a message.
    """
    message = get_object_or_404(Message, pk=object_id)
    if request.method == 'POST':
        if message.to_user == request.user:
            message.to_status = TO_STATUS_DELETED
        else:
            message.from_status = FROM_STATUS_DELETED
        message.save()
        return HttpResponseRedirect(reverse('messages:messages'))
    return render_to_response(template_name, {
        'message': message
    }, context_instance=RequestContext(request))


@login_required
def message_detail(request, object_id, template_name='messages/message_detail.html'):
    """
    Return a message.
    """
    message = get_object_or_404(Message, pk=object_id)
    content_type = ContentType.objects.get_for_model(message)
    thread_list = Message.objects.filter(object_id=message.object.pk, content_type=content_type).order_by('id')
    if message.to_user == request.user:
        message.to_status = TO_STATUS_READ
        message.save()
    return render_to_response(template_name, {
        'message': message,
        'thread_list': thread_list
    }, context_instance=RequestContext(request))
