from django.shortcuts import get_object_or_404

from basic.groups.decorators import *
from basic.groups.models import *
from basic.groups.forms import *
from basic.tools.shortcuts import render, redirect


def message_list(request, slug, topic_id, template_name='groups/messages/message_list.html'):
    """
    Returns a group topic message list page.

    Templates: ``groups/messages/message_list.html``
    Context:
        group
            Group object
        topic
            GroupTopic object
        message_list
            List of GroupMessage objects
    """
    group = get_object_or_404(Group, slug=slug, is_active=True)
    topic = get_object_or_404(GroupTopic, pk=topic_id, group=group, is_active=True)
    return render(request, template_name, {
        'group': group,
        'topic': topic,
        'message_list': topic.messages.all()
    })


def message_detail(request, slug, topic_id, message_id,
        template_name='groups/messages/message_detail.html'):
    """
    Returns a message detail page.

    Templates: ``groups/messages/message_detail.html``
    Context:
        group
            Group object
        topic
            GroupTopic object
        message
            GroupMessage object
    """
    group = get_object_or_404(Group, slug=slug, is_active=True)
    topic = get_object_or_404(GroupTopic, pk=topic_id, is_active=True)
    message = get_object_or_404(GroupMessage, pk=message_id, is_active=True)
    return render(request, template_name, {
        'group': group,
        'topic': topic,
        'message': message
    })


@membership_required
def message_create(request, slug, topic_id,
        template_name='groups/messages/message_form.html'):
    """
    Returns a group message form.

    Templates: ``groups/messages/message_form.html``
    Context:
        group
            Group object
        topic
            GroupTopic object
        form
            GroupMessageForm object
    """
    group = get_object_or_404(Group, slug=slug)
    topic = get_object_or_404(GroupTopic, pk=topic_id, group=group)
    if request.method == 'POST':
        form = GroupMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.user = request.user
            message.topic = topic
            message.save()
            return redirect(request, topic)
    else:
        form = GroupMessageForm()
    return render(request, template_name, {
        'group': group,
        'topic': topic,
        'form': form,
    })


@membership_required
def message_edit(request, slug, topic_id, message_id,
        template_name='groups/messages/message_form.html'):
    """
    Returns a group message edit form.

    Templates: ``groups/messages/message_form.html``
    Context:
        group
            Group object
        topic
            GroupTopic object
        message
            GroupMessage object
        form
            GroupMessageForm object
    """
    message = get_object_or_404(GroupMessage, pk=message_id, is_active=True)
    if request.method == 'POST':
        form = GroupMessageForm(request.POST, instance=message)
        if form.is_valid():
            form.save()
            return redirect(request, message.topic)
    else:
        form = GroupMessageForm(instance=message)
    return render(request, template_name, {
        'group': message.topic.group,
        'topic': message.topic,
        'message': message,
        'form': form,
    })


@membership_required
def message_remove(request, slug, topic_id, message_id,
        template_name='groups/messages/message_remove_confirm.html'):
    """
    Returns a message delete confirmation page.

    Templates: ``groups/messages/message_remove_confirm.html``
    Context:
        group
            Group object
        topic
            GroupTopic object
        message
            GroupMessage object
    """
    message = get_object_or_404(GroupMessage, pk=message_id, is_active=True)
    if request.method == 'POST':
        message.is_active = False
        message.save()
        return redirect(request, message.topic)
    return render(request, template_name, {
        'group': message.topic.group,
        'topic': message.topic,
        'message': message,
    })
