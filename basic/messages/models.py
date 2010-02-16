from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models import permalink
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericForeignKey


class Message(models.Model):
    """ Message model """
    FROM_STATUS_CHOICES = (
        (0, 'Draft'),
        (1, 'Sent'),
        (2, 'Deleted')
    )
    TO_STATUS_CHOICES = (
        (0, 'New'),
        (1, 'Read'),
        (2, 'Replied'),
        (3, 'Deleted')
    )
    from_user = models.ForeignKey(User, related_name='sent_messages')
    to_user = models.ForeignKey(User, related_name='messages')
    from_status = models.PositiveSmallIntegerField(choices=FROM_STATUS_CHOICES, blank=True, null=True, default=1)
    to_status = models.PositiveSmallIntegerField(choices=TO_STATUS_CHOICES, blank=True, null=True, default=0)
    subject = models.CharField(blank=True, max_length=255)
    message = models.TextField(blank=True)
    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)

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
