from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models import permalink
from django.contrib.auth.models import User
from django.contrib.sitemaps import ping_google
from django.conf import settings
from tagging.fields import TagField
from basic.blog.managers import PublicManager

import datetime
import tagging


class Category(models.Model):
    """Category model."""
    title       = models.CharField(_('title'), max_length=100)
    slug        = models.SlugField(_('slug'), unique=True)

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        db_table = 'blog_categories'
        ordering = ('title',)

    class Admin:
        pass

    def __unicode__(self):
        return u'%s' % self.title

    @permalink
    def get_absolute_url(self):
        return ('blog_category_detail', None, {'slug': self.slug})


class Post(models.Model):
    """Post model."""
    STATUS_CHOICES = (
        (1, _('Draft')),
        (2, _('Public')),
    )
    title           = models.CharField(_('title'), max_length=200)
    slug            = models.SlugField(_('slug'), unique_for_date='publish')
    author          = models.ForeignKey(User, blank=True, null=True)
    body            = models.TextField(_('body'), help_text='Use raw HTML.')
    tease           = models.TextField(_('tease'), blank=True, help_text='Use plain text (Only style tags allowed).')
    status          = models.IntegerField(_('status'), choices=STATUS_CHOICES, default=2)
    allow_comments  = models.BooleanField(_('allow comments'), default=True)
    publish         = models.DateTimeField(_('publish'), default=datetime.datetime.now)
    created         = models.DateTimeField(_('created'), auto_now_add=True)
    modified        = models.DateTimeField(_('modified'), auto_now=True)
    categories      = models.ManyToManyField(Category, blank=True)
    tags            = TagField()
    objects         = PublicManager()

    class Meta:
        verbose_name = _('post')
        verbose_name_plural = _('posts')
        db_table  = 'blog_posts'
        ordering  = ('-publish',)
        get_latest_by = 'publish'

    class Admin:
        list_display  = ('title', 'publish', 'status')
        list_filter   = ('publish', 'categories', 'status')
        search_fields = ('title', 'body')

    class ProxyMeta:
        title = 'title'
        description = 'body'
        tags = 'tags'
        pub_date = 'publish'
        active = {'status':2}

    def __unicode__(self):
        return u'%s' % self.title

    def save(self, *args, **kwargs):
        super(Post, self).save(*args, **kwargs)
        if getattr(settings, 'PING_GOOGLE', False):
            try:
                ping_google()
            except:
                pass

    @permalink
    def get_absolute_url(self):
        return ('blog_detail', None, {
            'year': self.publish.year,
            'month': self.publish.strftime('%b').lower(),
            'day': self.publish.day,
            'slug': self.slug
        })
    
    def get_previous_post(self):
        return self.get_previous_by_publish(status__gte=2)
    
    def get_next_post(self):
        return self.get_next_by_publish(status__gte=2)


class BlogRoll(models.Model):
    '''Other blogs you follow.'''
    
    name = models.CharField(max_length=100)
    url = models.URLField(verify_exists=False)
    sort_order =  models.PositiveIntegerField(default=0)
    
    def __unicode__(self):
        return self.name
        
    class Meta:
        ordering = ('sort_order','name',)
