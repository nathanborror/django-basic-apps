from django.db import models
from django.db.models import permalink
from django.conf import settings
from tagging.fields import TagField

import tagging


class AudioSet(models.Model):
    """AudioSet model"""
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField(blank=True)
    audios = models.ManyToManyField('Audio', related_name='audio_sets')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'media_audio_sets'

    def __unicode__(self):
        return '%s' % self.title

    @permalink
    def get_absolute_url(self):
        return ('audio_set_detail', None, { 'slug': self.slug })


class Audio(models.Model):
    """Audio model"""
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    still = models.FileField(upload_to='audio_stills', blank=True, help_text='An image that will be used as a thumbnail.')
    audio = models.FilePathField(path=settings.MEDIA_ROOT+'audios/', recursive=True)
    description = models.TextField(blank=True)
    tags = TagField()
    uploaded = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'media_audio'
        verbose_name_plural = 'audios'

    def __unicode__(self):
        return '%s' % self.title

    @permalink
    def get_absolute_url(self):
      return ('audio_detail', None, { 'slug': self.slug })


class PhotoSet(models.Model):
    """PhotoSet model"""
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField(blank=True)
    cover_photo = models.ForeignKey('Photo', blank=True, null=True)
    photos = models.ManyToManyField('Photo', related_name='photo_sets')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
      db_table = 'media_photo_sets'

    def __unicode__(self):
      return '%s' % self.title

    @permalink
    def get_absolute_url(self):
      return ('photo_set_detail', None, { 'slug': self.slug })


class Photo(models.Model):
    """Photo model"""
    LICENSES = (
        ('http://creativecommons.org/licenses/by/2.0/',         'CC Attribution'),
        ('http://creativecommons.org/licenses/by-nd/2.0/',      'CC Attribution-NoDerivs'),
        ('http://creativecommons.org/licenses/by-nc-nd/2.0/',   'CC Attribution-NonCommercial-NoDerivs'),
        ('http://creativecommons.org/licenses/by-nc/2.0/',      'CC Attribution-NonCommercial'),
        ('http://creativecommons.org/licenses/by-nc-sa/2.0/',   'CC Attribution-NonCommercial-ShareAlike'),
        ('http://creativecommons.org/licenses/by-sa/2.0/',      'CC Attribution-ShareAlike'),
    )
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    photo = models.FileField(upload_to="photos")
    taken_by = models.CharField(max_length=100, blank=True)
    license = models.URLField(blank=True, choices=LICENSES)
    description = models.TextField(blank=True)
    tags = TagField()
    uploaded = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    _exif = models.TextField(blank=True) 

    class Meta:
        db_table = 'media_photos'

    def _set_exif(self, d):
        self._exif = simplejson.dumps(d)

    def _get_exif(self):
        if self._exif:
            return simplejson.loads(self._exif)
        else:
            return {}

    exif = property(_get_exif, _set_exif, "Photo EXIF data, as a dict.")

    def __unicode__(self):
        return '%s' % self.title

    @property
    def url(self):
        return '%s%s' % (settings.MEDIA_URL, self.photo)

    @permalink
    def get_absolute_url(self):
        return ('photo_detail', None, { 'slug': self.slug })


class VideoSet(models.Model):
    """VideoSet model"""
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField(blank=True)
    videos = models.ManyToManyField('Video', related_name='video_sets')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'media_video_sets'

    def __unicode__(self):
        return '%s' % self.title

    @permalink
    def get_absolute_url(self):
        return ('video_set_detail', None, { 'slug': self.slug })


class Video(models.Model):
    """Video model"""
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    still = models.FileField(upload_to='video_stills', blank=True, help_text='An image that will be used as a thumbnail.')
    video = models.FilePathField(path=settings.MEDIA_ROOT+'videos/', recursive=True)
    description = models.TextField(blank=True)
    tags = TagField()
    uploaded = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'media_videos'

    def __unicode__(self):
        return '%s' % self.title

    @permalink
    def get_absolute_url(self):
        return ('video_detail', None, { 'slug': self.slug })