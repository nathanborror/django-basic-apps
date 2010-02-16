from django.shortcuts import get_object_or_404
from django.http import Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from readernaut.shortcuts import render
from basic.messages.models import Message
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
        message_list = Message.objects.filter(from_user=request.user, from_status=1)
    else:
        message_list = Message.objects.filter(to_user=request.user, to_status__in=(0,1,2))
    return render(request, template_name, {
        'message_list': message_list,
        'mailbox': mailbox
    })


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
    return render(request, template_name, {
        'form': form,
        'to_user': to_user
    })


@login_required
def message_remove(request):
    if request.method == 'POST':
        object_id = request.POST.get('object_id', '')
        try:
            message = Message.objects.get(pk=object_id, to_user=request.user)
            message.to_status = 3
        except Message.DoesNotExist:
            message = Message.objects.get(pk=object_id, from_user=request.user)
            message.from_status = 2
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
        message.to_status = 1
        message.save()
    return render(request, template_name, {
        'message': message,
        'mailbox': mailbox
    })