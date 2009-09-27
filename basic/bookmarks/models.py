from django.db import models
from django.utils.translation import ugettext_lazy as _
from tagging.fields import TagField


class Bookmark(models.Model):
    """Bookmarks model"""
    title = models.CharField(max_length=100, blank=True, null=True)
    slug = models.SlugField(_('slug'), unique=True)
    url = models.URLField(_('url'), unique=True)
    description = models.TextField(_('description'), )
    extended = models.TextField(_('extended'), blank=True)
    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)
    tags = TagField()

    class Meta:
        verbose_name = _('bookmark')
        verbose_name_plural = _('bookmarks')
        db_table = "bookmarks"

    def __unicode__(self):
        return self.url

    def get_absolute_url(self):
        return self.url
