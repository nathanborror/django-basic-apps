from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericForeignKey
from django.contrib.auth.models import User


class FlagType(models.Model):
    """ FlagType model """
    content_type = models.ForeignKey(ContentType, related_name='item')
    title = models.CharField(_('title'), blank=True, max_length=255)
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
    flag_type = models.ForeignKey(FlagType)
    object_id = models.IntegerField(_('object id'))
    user = models.ForeignKey(User)
    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)

    class Meta:
        verbose_name = _('flag')
        verbose_name_plural = _('flags')
        db_table = 'flags'

    def __unicode__(self):
        return '<Flagged item>'

    @property
    def object(self):
        model = self.flag_type.content_type.model_class()
        return model.objects.get(pk=self.object_id)