from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.db.models import permalink
from django.contrib.auth.models import User
from tagging.fields import TagField

import datetime
import dateutil


class PersonType(models.Model):
    """Person type model."""
    title = models.CharField(_('title'), max_length=100)
    slug = models.SlugField(_('slug'), unique=True)

    class Meta:
        verbose_name = _('person type')
        verbose_name_plural = _('person types')
        db_table = 'people_types'
        ordering = ('title',)

    def __unicode__(self):
        return '%s' % self.title

    @permalink
    def get_absolute_url(self):
        return ('person_type_detail', None, {'slug': self.slug})


class Person(models.Model):
    """Person model."""
    GENDER_CHOICES = (
        (1, 'Male'),
        (2, 'Female'),
    )
    first_name = models.CharField(_('first name'), blank=True, max_length=100)
    middle_name = models.CharField(_('middle name'), blank=True, max_length=100)
    last_name = models.CharField(_('last name'), blank=True, max_length=100)
    slug = models.SlugField(_('slug'), unique=True)
    user = models.ForeignKey(User, blank=True, null=True, help_text='If the person is an existing user of your site.')
    gender = models.PositiveSmallIntegerField(_('gender'), choices=GENDER_CHOICES, blank=True, null=True)
    mugshot = models.FileField(_('mugshot'), upload_to='mugshots', blank=True)
    mugshot_credit = models.CharField(_('mugshot credit'), blank=True, max_length=200)
    birth_date = models.DateField(_('birth date'), blank=True, null=True)
    person_types = models.ManyToManyField(PersonType, blank=True)
    website = models.URLField(_('website'), blank=True)

    class Meta:
        verbose_name = _('person')
        verbose_name_plural = _('people')
        db_table = 'people'
        ordering = ('last_name', 'first_name',)

    def __unicode__(self):
        return u'%s' % self.full_name

    @property
    def full_name(self):
        return u'%s %s' % (self.first_name, self.last_name)

    @property
    def age(self):
        TODAY = datetime.date.today()
        return u'%s' % dateutil.relativedelta(TODAY, self.birth_date).years

    @permalink
    def get_absolute_url(self):
        return ('person_detail', None, {'slug': self.slug})


class Quote(models.Model):
    """Quote model."""
    person = models.ForeignKey(Person)
    quote = models.TextField(_('quote'))
    source = models.CharField(_('source'), blank=True, max_length=255)

    class Meta:
        verbose_name = 'quote'
        verbose_name_plural = 'quotes'
        db_table = 'people_quotes'

    def __unicode__(self):
        return u'%s' % self.quote

    @permalink
    def get_absolute_url(self):
        return ('quote_detail', None, {'quote_id': self.pk})


class Conversation(models.Model):
    """A conversation between two or many people."""
    title = models.CharField(blank=True, max_length=200)

    def __unicode__(self):
        return self.title


class ConversationItem(models.Model):
    """An item within a conversation."""
    conversation      = models.ForeignKey(Conversation, related_name='items')
    order             = models.PositiveSmallIntegerField()
    speaker           = models.ForeignKey(Person)
    quote             = models.TextField()

    class Meta:
        ordering = ('conversation', 'order')
        unique_together = (('conversation', 'order'),)

    def __unicode__(self):
        return u'%s: %s' % (self.speaker.first_name, self.quote)