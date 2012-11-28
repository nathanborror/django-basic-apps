from django.db import models
from django.db.models import permalink
from django.conf import settings
from basic.people.models import Person


class Genre(models.Model):
    """Genre model"""
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    class Meta:
        db_table = 'movie_genres'
        ordering = ('title',)

    def __unicode__(self):
        return '%s' % self.title

    @permalink
    def get_absolute_url(self):
        return ('movie_genre_detail', None, { 'slug': self.slug })


class Studio(models.Model):
    """Studio model"""
    title = models.CharField(max_length=100)
    prefix = models.CharField(max_length=20, blank=True)
    slug = models.SlugField(unique=True)
    website = models.URLField(blank=True)

    class Meta:
        db_table = 'movie_studios'
        ordering = ('title',)

    def __unicode__(self):
        return '%s' % self.full_title

    @property
    def full_title(self):
        return '%s %s' % (self.prefix, self.title)

    @permalink
    def get_absolute_url(self):
        return ('movie_studio_detail', None, { 'slug': self.slug })


class Movie(models.Model):
    """Movie model"""
    title = models.CharField(max_length=255)
    prefix = models.CharField(max_length=20, blank=True)
    subtitle = models.CharField(blank=True, max_length=255)
    slug = models.SlugField(unique=True)
    directors = models.ManyToManyField(Person, limit_choices_to={'person_types__slug__exact': 'director'}, blank=True)
    studio = models.ForeignKey(Studio, blank=True, null=True)
    released = models.DateField(blank=True, null=True)
    asin = models.CharField(blank=True, max_length=100)
    cover = models.FileField(upload_to='films', blank=True)
    review = models.TextField(blank=True)
    genre = models.ManyToManyField(Genre, blank=True)

    class Meta:
        db_table = 'movies'
        ordering = ('title',)

    def __unicode__(self):
        return '%s' % self.full_title

    @property
    def full_title(self):
        return '%s %s' % (self.prefix, self.title)

    @permalink
    def get_absolute_url(self):
        return ('movie_detail', None, { 'slug': self.slug })

    @property
    def amazon_url(self):
        try:
            return 'http://www.amazon.com/dp/%s/?%s' % (self.asin, settings.AMAZON_AFFILIATE_EXTENTION)
        except:
            return 'http://www.amazon.com/dp/%s/' % self.asin

    @property
    def cover_url(self):
        return '%s%s' % (settings.MEDIA_URL, self.cover)