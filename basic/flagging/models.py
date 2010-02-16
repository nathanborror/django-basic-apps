from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericForeignKey
from django.contrib.auth.models import User


class FlagType(models.Model):
    """ FlagType model """
    title = models.CharField(_('title'), blank=False, max_length=255)
    slug = models.SlugField()
    description = models.TextField(_('description'), blank=True)

    class Meta:
        verbose_name = _('flag type')
        verbose_name_plural = _('flag types')
        db_table = 'flag_types'

    def __unicode__(self):
        return self.title


class Flag(models.Model):
    """ Flag model """
    content_type = models.ForeignKey(ContentType, related_name='flags')
    object_id = models.IntegerField()
    object = GenericForeignKey()
    flag_type = models.ForeignKey(FlagType)
    user = models.ForeignKey(User)
    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)

    class Meta:
        verbose_name = _('flag')
        verbose_name_plural = _('flags')
        db_table = 'flags'

    def __unicode__(self):
        return '<Flagged item>'