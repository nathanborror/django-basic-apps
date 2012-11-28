from django.db import models
from django.db.models import permalink
from django.conf import settings
from django.contrib.auth.models import User
from basic.people.models import Person


class Genre(models.Model):
    """Genre model"""
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    class Meta:
        db_table = 'book_genres'
        ordering = ('title',)

    def __unicode__(self):
        return '%s' % self.title

    @permalink
    def get_absolute_url(self):
        return ('book_genre_detail', None, { 'slug': self.slug })


class Publisher(models.Model):
    """Publisher"""
    title = models.CharField(max_length=100)
    prefix = models.CharField(max_length=20, blank=True)
    slug = models.SlugField(unique=True)
    website = models.URLField(blank=True)

    class Meta:
        db_table = 'book_publishers'
        ordering = ('title',)

    def __unicode__(self):
        return '%s' % self.full_title

    @property
    def full_title(self):
        return '%s %s' % (self.prefix, self.title)

    @permalink
    def get_absolute_url(self):
        return ('book_publisher_detail', None, { 'slug':self.slug })


class Book(models.Model):
    """Listing of books"""
    title = models.CharField(max_length=255)
    prefix = models.CharField(max_length=20, blank=True)
    subtitle = models.CharField(blank=True, max_length=255)
    slug = models.SlugField(unique=True)
    authors = models.ManyToManyField(Person, limit_choices_to={'person_types__slug__exact': 'author'}, related_name='books')
    isbn = models.CharField(max_length=14, blank=True)
    pages = models.PositiveSmallIntegerField(blank=True, null=True, default=0)
    publisher = models.ForeignKey(Publisher, blank=True, null=True)
    published = models.DateField(blank=True, null=True)
    cover = models.FileField(upload_to='books', blank=True)
    description = models.TextField(blank=True)
    genre = models.ManyToManyField(Genre, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'books'
        ordering = ('title',)

    def __unicode__(self):
        return '%s' % self.full_title

    @property
    def full_title(self):
        if self.prefix:
            return '%s %s' % (self.prefix, self.title)
        else:
            return '%s' % self.title

    @permalink
    def get_absolute_url(self):
        return ('book_detail', None, { 'slug': self.slug })

    @property
    def amazon_url(self):
        if self.isbn:
            try:
                return 'http://www.amazon.com/dp/%s/?%s' % (self.isbn, settings.AMAZON_AFFILIATE_EXTENTION)
            except:
                return 'http://www.amazon.com/dp/%s/' % self.isbn
        return ''


class Highlight(models.Model):
    """Highlights from books"""
    user = models.ForeignKey(User)
    book = models.ForeignKey(Book)
    highlight = models.TextField()
    page = models.CharField(blank=True, max_length=20)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'book_highlights'

    def __unicode__(self):
        return '%s' % self.highlight

    @permalink
    def get_absolute_url(self):
        return ('book_detail', None, { 'slug': self.book.slug })


class Page(models.Model):
    """Page model"""
    user = models.ForeignKey(User)
    book = models.ForeignKey(Book)
    current_page = models.PositiveSmallIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'book_read_pages'
        ordering = ('-created',)

    def __unicode__(self):
        return '%s' % self.current_page