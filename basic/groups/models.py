from django.db import models
from django.db.models import permalink
from django.contrib.auth.models import User

from basic.groups.managers import *
from basic.tools.shortcuts import get_image_path


class Group(models.Model):
    """ Group model """
    title = models.CharField(blank=False, max_length=255)
    slug = models.SlugField(unique=True, help_text="Used for the Group URL: http://example.com/groups/the-club/")
    tease = models.TextField(blank=True, help_text="Brief explaination of what this group is. Shows up when the group is listed amoung other groups.")
    creator = models.ForeignKey(User, related_name='created_groups', help_text="Serves as a record as who the original creator was in case ownership is transfered.")
    icon = models.FileField(upload_to=get_image_path, blank=True, help_text="Needs to be larger than 120x120 pixels.")
    invite_only = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.title

    @permalink
    def get_absolute_url(self):
        return ('groups:group', None, {'slug': self.slug})

    def owners(self):
        return self.members.filter(status=0)

    def moderators(self):
        return self.members.filter(status=1)

    def is_member(self, user):
        try:
            member = self.members.get(user=user)
            return member
        except:
            return None


class GroupPage(models.Model):
    """ GroupPage model """
    group = models.ForeignKey(Group, related_name='group_texts')
    title = models.CharField(blank=True, max_length=100)
    slug = models.SlugField()
    body = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.title

    @permalink
    def get_absolute_url(self):
        return ('groups:page', None, {
            'slug': self.group.slug,
            'page_slug': self.slug
        })


class GroupTopic(models.Model):
    """ GroupTopic model """
    group = models.ForeignKey(Group, related_name='topics')
    user = models.ForeignKey(User, related_name='group_topics')
    title = models.CharField(blank=False, max_length=100)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-id',)

    def __unicode__(self):
        return self.title

    @permalink
    def get_absolute_url(self):
        return ('groups:topic', None, {
            'slug': self.group.slug,
            'topic_id': self.pk
        })


class GroupMessage(models.Model):
    """ GroupMessage model """
    topic = models.ForeignKey(GroupTopic, related_name="messages")
    user = models.ForeignKey(User)
    message = models.TextField(blank=False)
    is_active = models.BooleanField(default=True)
    objects = GroupMessageManager()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.message

    @permalink
    def get_absolute_url(self):
        return ('groups:message', None, {
            'slug': self.topic.group.slug,
            'topic_id': self.topic.pk,
            'message_id': self.pk
        })


class GroupMember(models.Model):
    """ GroupMember model """
    user = models.ForeignKey(User, related_name='group_memberships')
    group = models.ForeignKey(Group, related_name='members')
    status = models.PositiveSmallIntegerField(choices=((0, 'Owner'),(1, 'Moderator'),(2, 'Member')), default=2)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    objects = GroupMemberManager()

    class Meta:
        unique_together = (('user', 'group'),)

    def __unicode__(self):
        return '%s' % self.user
