from django.db import models
from django.utils.translation import ugettext_lazy as _
from tagging.fields import TagField


class Bookmark(models.Model):
  """ Simple model for storing bookmarks """
  url             = models.URLField(_('url'), unique=True)
  description     = models.TextField(_('description'), )
  extended        = models.TextField(_('extended'), blank=True)
  created         = models.DateTimeField(_('created'), auto_now_add=True)
  modified        = models.DateTimeField(_('modified'), auto_now=True)
  tags            = TagField()
  
  class Meta:
    verbose_name = _('bookmark')
    verbose_name_plural = _('bookmarks')
    db_table = "bookmarks"

  class Admin:
    list_display = ('url', 'description')
    search_fields = ('url', 'description', 'extended')

  def __unicode__(self):
    return self.url
