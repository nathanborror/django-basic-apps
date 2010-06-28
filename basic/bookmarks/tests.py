"""
>>> from django.test import Client
>>> from basic.bookmarks.models import Bookmark
>>> from django.core.urlresolvers import reverse

>>> client = Client()

>>> response = client.get(reverse('bookmark_index'))
>>> response.status_code
200

>>> bookmark = Bookmark(url='http://www.google.com', description='Django book', extended='Great resource!')
>>> bookmark.save()

"""