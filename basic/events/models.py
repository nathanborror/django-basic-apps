import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models import permalink
from django.contrib.auth.models import User
from tagging.fields import TagField
from basic.places.models import Place


class Event(models.Model):
    """Event model"""
    title = models.CharField(max_length=200)
    slug = models.SlugField()
    place = models.ForeignKey(Place, blank=True, null=True)
    one_off_place = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    submitted_by = models.ForeignKey(User, blank=True, null=True)
    tags = TagField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('event')
        verbose_name_plural = _('events')
        db_table = 'events'

    def __unicode__(self):
        return self.title


class EventTime(models.Model):
    """EventTime model"""
    event = models.ForeignKey(Event, related_name='event_times')
    start = models.DateTimeField()
    end = models.DateTimeField(blank=True, null=True)
    is_all_day = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('event time')
        verbose_name_plural = _('event times')
        db_table = 'event_times'

    @property
    def is_past(self):
        NOW = datetime.date.now()
        if self.start < NOW:
            return True
        return False

    def __unicode__(self):
        return u'%s' % self.event.title

    @permalink
    def get_absolute_url(self):
        return ('event_detail', None, {
            'year': self.start.year,
            'month': self.start.strftime('%b').lower(),
            'day': self.start.day,
            'slug': self.event.slug,
            'event_id': self.event.id
        })