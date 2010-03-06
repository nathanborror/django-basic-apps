from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic import date_based
from django.db.models import Q

from basic.groups.decorators import *
from basic.groups.models import *
from basic.groups.forms import *


def group_list(request, username=None, segment=None, template_name='groups/group_list.html'):
    """
    Returns a group list page.

    Templates: ``groups/group_list.html``
    Context:
        group_list
            Group object list
    """
    group_list = Group.objects.filter(is_active=True)
    return render_to_response(template_name, {
        'group_list': group_list
    }, context_instance=RequestContext(request))


@login_required
def group_create(request, template_name='groups/group_form.html'):
    """
    Returns a group form page.

    Templates: ``groups/group_form.html``
    Context:
        form
            GroupForm object
    """
    if request.method == 'POST':
        form = GroupForm(request.POST, request.FILES)
        if form.is_valid():
            group = form.save(commit=False)
            group.creator = request.user
            group.save()

            creator = GroupMember.objects.create(user=request.user, group=group, status=0)
            return HttpResponseRedirect(group.get_absolute_url())
    else:
        form = GroupForm()
    return render_to_response(template_name, {'form': form}, context_instance=RequestContext(request))


def group_detail(request, slug, template_name='groups/group_detail.html'):
    """
    Returns a group detail page.

    Templates: ``groups/group_detail.html``
    Context:
        group
            Group object
    """
    group = get_object_or_404(Group, slug=slug, is_active=True)
    if group.invite_only and not GroupMember.objects.is_member(group, request.user):
        return HttpResponseRedirect(reverse('group_join', kwargs={'slug': group.slug}))
    return render_to_response(template_name, {
        'group': group,
        'topic_list': group.topics.all(),
    }, context_instance=RequestContext(request))


@ownership_required
def group_edit(request, slug, template_name='groups/group_form.html'):
    """
    Returns a group form page.

    Templates: ``groups/group_form.html``
    Context:
        form
            GroupForm object
        group
            Group object
    """
    group = get_object_or_404(Group, slug=slug, creator=request.user)
    if request.method == 'POST':
        form = GroupForm(request.POST, request.FILES, instance=group)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(group.get_absolute_url())
    else:
        form = GroupForm(instance=group)
    return render_to_response(template_name, {
        'form': form,
        'group': group
    }, context_instance=RequestContext(request))


@ownership_required
def group_remove(request, slug, template_name='groups/group_remove_confirm.html'):
    """
    Returns a group delete confirmation page.

    Templates: ``groups/group_remove_confirm.html``
    Context:
        group
            Group object
    """
    group = get_object_or_404(Group, slug=slug, creator=request.user)
    if request.method == 'POST':
        group.is_active = False
        group.save()
        return HttpResponseRedirect(reverse('groups'))
    return render_to_response(template_name, {'group': group}, context_instance=RequestContext(request))


def group_page(request, slug, page_slug, template_name='groups/group_page.html'):
    """
    Returns a group page.
    
    Templates: ``groups/group_page.html``
    Context:
        group
            Group object
        page
            GroupPage object
    """
    group = get_object_or_404(Group, slug=slug)
    page = get_object_or_404(GroupPage, group=group, slug=page_slug)
    return render_to_response(template_name, {
        'group': group,
        'page': page
    }, context_instance=RequestContext(request))


@ownership_required
def group_page_create(request, slug, page_slug,
            template_name='groups/group_page_form.html'):
    group = get_object_or_404(Group, slug=slug)
    form = GroupPageForm(initial={'group': group})

    if request.method == 'POST':
        form = GroupPageForm(request.POST)
        if form.is_valid():
            page = form.save()
            return HttpResponseRedirect(page.get_absolute_url())

    return render_to_response(template_name, {
        'group': group,
        'form': form
    }, context_instance=RequestContext(request))


@ownership_required
def group_page_edit(request, slug, page_slug,
            template_name='groups/group_page_form.html'):
    group = get_object_or_404(Group, slug=slug)
    page = get_object_or_404(GroupPage, group=group, slug=page_slug)
    form = GroupPageForm(instance=page)

    if request.method == 'POST':
        form = GroupPageForm(request.POST)
        if form.is_valid():
            page = form.save()
            return HttpResponseRedirect(page.get_absolute_url())

    return render_to_response(template_name, {
        'group': group,
        'page': page,
        'form': form
    }, context_instance=RequestContext(request))


@ownership_required
def group_page_remove(request, slug, page_slug,
            template_name='groups/group_page_remove_confirm.html'):
    group = get_object_or_404(Group, slug=slug)
    page = get_object_or_404(GroupPage, group=group, slug=page_slug)

    if request.method == 'POST':
        page.delete()
        return HttpResponseRedirect(group.get_absolute_url())

    return render_to_response(template_name, {
        'group': group,
        'page': page
    }, context_instance=RequestContext(request))


#
# Group members
#

def group_members(request, slug, template_name='groups/group_members.html'):
    """
    Returns members of a group.

    Templates: ``groups/group_members.html``
    Context:
        group
            Group object
        member_list
            User objects
    """
    group = get_object_or_404(Group, slug=slug, is_active=True)
    member_list = group.members.all()
    return render_to_response(template_name, {
        'group': group,
        'member_list': member_list
    }, context_instance=RequestContext(request))


@login_required
def group_join(request, slug, template_name='groups/group_join_confirm.html'):
    """
    Returns a group join confirmation page.

    Templates: ``groups/group_join_confirm.html``
    Context:
        group
            Group object
    """
    group = get_object_or_404(Group, slug=slug, is_active=True)
    if request.method == 'POST':
        membership = GroupMember(group=group, user=request.user)
        membership.save()
        return HttpResponseRedirect(group.get_absolute_url())
    return render_to_response(template_name, {'group': group}, context_instance=RequestContext(request))


@membership_required
def group_invite(request, slug, template_name='groups/group_invite.html'):
    """
    Returns an invite form.
    
    Templates: ``groups/group_invite.html``
    Context:
        form
            InviteForm object
    """
    group = get_object_or_404(Group, slug=slug, is_active=True)
    form = InviteForm(initial={'group': group.pk, 'user': request.user.pk})
    return render_to_response(template_name, {
        'group': group,
        'form': form
    }, context_instance=RequestContext(request))


#
# Group topics
#

def topic_list(request, slug, template_name='groups/topic_list.html'):
    """
    Returns a group topic list page.

    Templates: ``groups/topic_list.html``
    Context:
        group
            Group object
        topic_list
            GroupTopic object list
    """
    group = get_object_or_404(Group, slug=slug, is_active=True)
    topic_list = GroupTopic.objects.filter(group=group, is_active=True)
    return render_to_response(template_name, {
        'group': group,
        'topic_list': topic_list
    }, context_instance=RequestContext(request))


@membership_required
def topic_create(request, slug, template_name='groups/topic_form.html'):
    """
    Returns a group topic form page.

    Templates: ``groups/topic_form.html``
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
            return HttpResponseRedirect(topic.get_absolute_url())
    else:
        form = GroupTopicForm()
    return render_to_response(template_name, {
        'form': form,
        'group': group
    }, context_instance=RequestContext(request))


def topic_detail(request, slug, topic_id, template_name='groups/topic_detail.html'):
    """
    Returns a group topic detail page.

    Templates: ``groups/topic_detail.html``
    Context:
        topic
            GroupTopic object
        group
            Group object
    """
    group = get_object_or_404(Group, slug=slug, is_active=True)
    topic = get_object_or_404(GroupTopic, pk=topic_id, is_active=True)
    message_form = GroupMessageForm()
    return render_to_response(template_name, {
        'group': group,
        'topic': topic,
        'message_form': message_form,
    }, context_instance=RequestContext(request))


@membership_required
def topic_edit(request, topic_id, template_name='groups/topic_form.html'):
    """
    Returns a group topic form page.

    Templates: ``groups/topic_form.html``
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
            return HttpResponseRedirect(topic.get_absolute_url())
    else:
        form = GroupTopicForm(instance=topic)
    return render_to_response(template_name, {
        'form': form,
        'group': group,
        'topic': topic
    }, context_instance=RequestContext(request))


@membership_required
def topic_remove(request, topic_id, template_name='groups/topic_remove_confirm.html'):
    """
    Returns a group topic delete confirmation page.

    Templates: ``groups/topic_remove_confirm.html``
    Context:
        topic
            GroupTopic object
    """
    group = get_object_or_404(Group, slug=slug)
    topic = get_object_or_404(GroupTopic, pk=topic_id, group=group, user=request.user)
    if request.method == 'POST':
        topic.is_active = False
        topic.save()
        return HttpResponseRedirect(group.get_absolute_url())
    return render_to_response(template_name, {'topic': topic}, context_instance=RequestContext(request))


def topic_moderate(request, topic_id, template_name='groups/topic_moderate_confirm.html'):
    pass


#
# Group messages
#

def message_detail(request, slug, topic_id, message_id, template_name='groups/message_detail.html'):
    """
    Returns a message detail page.

    Templates: ``groups/message_detail.html``
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
    return render_to_response(template_name, {
        'group': group,
        'topic': topic,
        'message': message
    }, context_instance=RequestContext(request))


@membership_required
def message_create(request, slug, topic_id, template_name='groups/message_form.html'):
    """
    Returns a group message form.

    Templates: ``groups/message_form.html``
    Context:
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
            return HttpResponseRedirect(topic.get_absolute_url())
    else:
        form = GroupMessageForm()
    return render_to_response(template_name, {
        'form': form,
        'group': group,
        'topic': topic,
    }, context_instance=RequestContext(request))


@membership_required
def message_edit(request, message_id, template_name='groups/message_form.html'):
    """
    Returns a group message edit form.

    Templates: ``groups/message_form.html``
    Context:
        form
            GroupMessageForm object
        message
            GroupMessage object
    """
    message = get_object_or_404(GroupMessage, pk=message_id, is_active=True)
    if request.method == 'POST':
        form = GroupMessageForm(request.POST, instance=message)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(message.topic.get_absolute_url())
    else:
        form = GroupMessageForm(instance=message)
    return render_to_response(template_name, {
        'form': form,
        'message': message,
        'group': message.topic.group,
        'topic': message.topic
    }, context_instance=RequestContext(request))


@membership_required
def message_remove(request, message_id, template_name='groups/message_remove_confirm.html'):
    """
    Returns a message delete confirmation page.

    Templates: ``groups/message_remove_confirm.html``
    Context:
        message
            GroupMessage object
    """
    message = get_object_or_404(GroupMessage, pk=message_id, is_active=True)
    if request.method == 'POST':
        message.is_active = False
        message.save()
        return HttpResponseRedirect(message.topic.get_absolute_url())
    return render_to_response(template_name, {
        'message': message,
        'group': message.topic.group,
        'topic': message.topic
    }, context_instance=RequestContext(request))


def message_moderate(request, message_id, template_name='groups/message_moderate_confirm.html'):
    pass