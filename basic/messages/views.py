from django.shortcuts import get_object_or_404, render_to_response
from django.http import Http404, HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from basic.messages.models import Message
from basic.messages.forms import MessageForm

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
        'mailbox': mailbox
    }, context_instance=RequestContext(request))


@login_required
def message_create(request, username=None, template_name='messages/message_form.html'):
    """
    Handles a new message and displays a form.

    Template:: ``messages/message_form.html``
    Context:
        form
            MessageForm object
    """
    if username:
        to_user = get_object_or_404(User, username=username)
    else:
        to_user = None
    form = MessageForm(request.POST or None, initial={'to_user': to_user})
    if form.is_valid():
        message = form.save(commit=False)
        message.from_user = request.user
        message.save()
        return HttpResponseRedirect(reverse('messages:messages'))
    return render_to_response(template_name, {
        'form': form,
        'to_user': to_user
    }, context_instance=RequestContext(request))


@login_required
def message_remove(request, object_id, template_name='messages/message_remove_confirm.html'):
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
    message = get_object_or_404(Message, pk=object_id)
    if message.to_user == request.user:
        message.to_status = TO_STATUS_READ
        message.save()
    return render_to_response(template_name, {
        'message': message
    }, context_instance=RequestContext(request))
