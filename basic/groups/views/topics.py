from django.shortcuts import get_object_or_404

from basic.groups.decorators import *
from basic.groups.models import *
from basic.groups.forms import *
from basic.tools.shortcuts import render, redirect


def topic_list(request, slug, template_name='groups/topics/topic_list.html'):
    """
    Returns a group topic list page.

    Templates: ``groups/topics/topic_list.html``
    Context:
        group
            Group object
        topic_list
            GroupTopic object list
    """
    group = get_object_or_404(Group, slug=slug, is_active=True)
    topic_list = GroupTopic.objects.filter(group=group, is_active=True)
    return render(request, template_name, {
        'group': group,
        'topic_list': topic_list
    })


@membership_required
def topic_create(request, slug, template_name='groups/topics/topic_form.html'):
    """
    Returns a group topic form page.

    Templates: ``groups/topics/topic_form.html``
    Context:
        form
            GroupTopicForm object
    """
    group = get_object_or_404(Group, slug=slug)
    if request.method == 'POST':
        form = GroupTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.user = request.user
            topic.group = group
            topic.save()
            return redirect(request, topic)
    else:
        form = GroupTopicForm()
    return render(request, template_name, {
        'form': form,
        'group': group
    })


def topic_detail(request, slug, topic_id,
        template_name='groups/topics/topic_detail.html'):
    """
    Returns a group topic detail page.

    Templates: ``groups/topics/topic_detail.html``
    Context:
        topic
            GroupTopic object
        group
            Group object
    """
    group = get_object_or_404(Group, slug=slug, is_active=True)
    topic = get_object_or_404(GroupTopic, pk=topic_id, is_active=True)
    message_form = GroupMessageForm()
    return render(request, template_name, {
        'group': group,
        'topic': topic,
        'message_form': message_form,
    })


@membership_required
def topic_edit(request, slug, topic_id,
        template_name='groups/topics/topic_form.html'):
    """
    Returns a group topic form page.

    Templates: ``groups/topics/topic_form.html``
    Context:
        form
            GroupTopicForm object
        topic
            GroupTopic object
    """
    group = get_object_or_404(Group, slug=slug)
    topic = get_object_or_404(GroupTopic, pk=topic_id, group=group, user=request.user)
    if request.method == 'POST':
        form = GroupTopicForm(request.POST, instance=topic)
        if form.is_valid():
            form.save()
            return redirect(request, topic)
    else:
        form = GroupTopicForm(instance=topic)
    return render(request, template_name, {
        'form': form,
        'group': group,
        'topic': topic
    })


@membership_required
def topic_remove(request, slug, topic_id,
        template_name='groups/topics/topic_remove_confirm.html'):
    """
    Returns a group topic delete confirmation page.

    Templates: ``groups/topics/topic_remove_confirm.html``
    Context:
        topic
            GroupTopic object
    """
    group = get_object_or_404(Group, slug=slug)
    topic = get_object_or_404(GroupTopic, pk=topic_id, group=group, user=request.user)
    if request.method == 'POST':
        topic.is_active = False
        topic.save()
        return redirect(request, group)
    return render(request, template_name, {'topic': topic})
