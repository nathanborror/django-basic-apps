from django.shortcuts import get_object_or_404, render_to_response
from django.http import Http404, HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from basic.messages.models import Message, FROM_STATUS_DRAFT, FROM_STATUS_SENT,
    FROM_STATUS_DELETED, TO_STATUS_NEW, TO_STATUS_READ, TO_STATUS_REPLIED,
    TO_STATUS_DELETED
from basic.messages.forms import MessageForm

@login_required
def message_list(request, mailbox='inbox', template_name='messages/message_list.html'):
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
        message_list = Message.objects.filter(from_user=request.user, from_status=FROM_STATUS_SENT)
    else:
        message_list = Message.objects.filter(to_user=request.user, to_status__in=(TO_STATUS_NEW,TO_STATUS_READ,TO_STATUS_REPLIED))
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
        return HttpResponseRedirect(reverse('user_messages'))
    return render_to_response(template_name, {
        'form': form,
        'to_user': to_user
    }, context_instance=RequestContext(request))


@login_required
def message_remove(request):
    if request.method == 'POST':
        object_id = request.POST.get('object_id', '')
        try:
            message = Message.objects.get(pk=object_id, to_user=request.user)
            message.to_status = TO_STATUS_DELETED
        except Message.DoesNotExist:
            message = Message.objects.get(pk=object_id, from_user=request.user)
            message.from_status = FROM_STATUS_DELETED
        except Message.DoesNotExist:
            raise Http404

        message.save()
        return HttpResponseRedirect(reverse('user_messages'))
    else:
        raise Http404


@login_required
def message_detail(request, mailbox, object_id, template_name='messages/message_detail.html'):
    if mailbox == 'sent':
        message = get_object_or_404(Message, pk=object_id, from_user=request.user)
    elif mailbox == 'inbox':
        message = get_object_or_404(Message, pk=object_id, to_user=request.user)
        message.to_status = TO_STATUS_READ
        message.save()
    return render_to_response(template_name, {
        'message': message,
        'mailbox': mailbox
    }, context_instance=RequestContext(request))