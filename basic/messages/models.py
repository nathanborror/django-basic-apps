from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models import permalink, Manager, Q
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericForeignKey

FROM_STATUS_DRAFT = 0
FROM_STATUS_SENT = 1
FROM_STATUS_DELETED = 2

TO_STATUS_NEW = 0
TO_STATUS_READ = 1
TO_STATUS_REPLIED = 2
TO_STATUS_DELETED = 3


class MessageManager(Manager):
    """Returns messages according to message status"""

    def new(self, user):
        return self.filter(to_user=user, to_status=TO_STATUS_NEW)

    def sent(self, user):
        return self.filter(from_user=user, from_status=FROM_STATUS_SENT)

    def trash(self, user):
        return self.filter(Q(to_user=user, to_status=TO_STATUS_DELETED) |
            Q(from_user=user, from_status=FROM_STATUS_DELETED))

    def archive(self, user):
        return self.filter(to_user=user).exclude(to_status=TO_STATUS_DELETED)


class Message(models.Model):
    """ Message model """
    FROM_STATUS_CHOICES = (
        (FROM_STATUS_DRAFT, 'Draft'),
        (FROM_STATUS_SENT, 'Sent'),
        (FROM_STATUS_DELETED, 'Deleted')
    )
    TO_STATUS_CHOICES = (
        (TO_STATUS_NEW, 'New'),
        (TO_STATUS_READ, 'Read'),
        (TO_STATUS_REPLIED, 'Replied'),
        (TO_STATUS_DELETED, 'Deleted')
    )
    from_user = models.ForeignKey(User, related_name='sent_messages')
    to_user = models.ForeignKey(User, related_name='messages')
    from_status = models.PositiveSmallIntegerField(choices=FROM_STATUS_CHOICES, blank=True, null=True, default=1)
    to_status = models.PositiveSmallIntegerField(choices=TO_STATUS_CHOICES, blank=True, null=True, default=0)
    subject = models.CharField(blank=True, max_length=255)
    message = models.TextField(blank=True)
    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)
    objects = MessageManager()

    content_type = models.ForeignKey(ContentType, blank=True, null=True, related_name='messages')
    object_id = models.IntegerField(blank=True, null=True)
    object = GenericForeignKey()

    class Meta:
        verbose_name = _('message')
        verbose_name_plural = _('messages')
        db_table = 'messages'
        ordering = ('-id',)

    def __unicode__(self):
        return u'<Message>'

    @permalink
    def get_absolute_url(self):
        return ('messages:message', None, {'object_id': self.pk})

    @property
    def is_new(self):
        if self.to_status == TO_STATUS_NEW:
            return True
        return False
