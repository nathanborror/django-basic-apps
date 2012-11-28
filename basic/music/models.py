from django.db import models
from django.db.models import permalink
from django.conf import settings
from basic.people.models import Person


class Genre(models.Model):
    """Genre model"""
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    class Meta:
        db_table = 'music_genres'
        ordering = ('title',)

    def __unicode__(self):
        return '%s' % self.title

    @permalink
    def get_absolute_url(self):
        return ('music_genre_detail', None, { 'slug': self.slug })


class Label(models.Model):
    """Label model"""
    title = models.CharField(max_length=100)
    prefix = models.CharField(max_length=20, blank=True)
    slug = models.SlugField(unique=True)
    website = models.URLField(blank=True)

    class Meta:
        db_table = 'music_labels'
        ordering = ('title',)

    def __unicode__(self):
        return '%s' % self.full_title

    @property
    def full_title(self):
        return '%s %s' % (self.prefix, self.title)

    @permalink
    def get_absolute_url(self):
        return ('music_label_detail', None, { 'slug': self.slug })


class Band(models.Model):
    """Band model"""
    title = models.CharField(max_length=100)
    prefix = models.CharField(max_length=20, blank=True)
    slug = models.SlugField(unique=True)
    musicians = models.ManyToManyField(Person, blank=True, limit_choices_to={'person_types__slug__exact': 'musician'})
    website = models.URLField(blank=True)

    class Meta:
        db_table = 'music_bands'
        ordering = ('title',)

    def __unicode__(self):
        return '%s' % self.full_title

    @property
    def full_title(self):
        return '%s %s' % (self.prefix, self.title)

    @permalink
    def get_absolute_url(self):
        return ('music_band_detail', None, { 'slug': self.slug })


class Album(models.Model):
    """Album model"""
    title = models.CharField(max_length=255)
    prefix = models.CharField(max_length=20, blank=True)
    subtitle = models.CharField(blank=True, max_length=255)
    slug = models.SlugField()
    band = models.ForeignKey(Band, blank=True)
    label = models.ForeignKey(Label, blank=True)
    asin = models.CharField(max_length=14, blank=True)
    release_date = models.DateField(blank=True, null=True)
    cover = models.FileField(upload_to='albums', blank=True)
    review = models.TextField(blank=True)
    genre = models.ManyToManyField(Genre, blank=True)
    is_ep = models.BooleanField(default=False)
    is_compilation = models.BooleanField(default=False)

    class Meta:
        db_table = 'music_albums'
        ordering = ('title',)

    def __unicode__(self):
        return '%s' % self.full_title

    @permalink
    def get_absolute_url(self):
        return ('music_album_detail', None, { 'slug': self.slug })

    @property
    def full_title(self):
        return '%s %s' % (self.prefix, self.title)

    @property
    def cover_url(self):
        return '%s%s' % (settings.MEDIA_URL, self.cover)

    @property
    def amazon_url(self):
        try:
            return 'http://www.amazon.com/dp/%s/?%s' % (self.asin, settings.AMAZON_AFFILIATE_EXTENTION)
        except:
            return 'http://www.amazon.com/dp/%s/' % self.asin


class Track(models.Model):
    """Tracks model"""
    album = models.ForeignKey(Album, blank=True, null=True, related_name='tracks')
    band = models.ForeignKey(Band, blank=True, null=True, related_name='tracks')
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    mp3 = models.FilePathField(path=settings.MEDIA_ROOT+'tracks', match='.*\.mp3$')

    class Meta:
        db_table = 'music_tracks'
        ordering = ('title',)

    def __unicode__(self):
        return '%s' % self.title

    @permalink
    def get_absolute_url(self):
        return ('music_track_detail', None, { 'slug': self.slug })

    @property
    def mp3_url(self):
        return self.mp3.replace(settings.MEDIA_ROOT, settings.MEDIA_URL)