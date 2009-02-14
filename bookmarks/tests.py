"""
>>> from django.test import Client
>>> from basic.bookmarks.models import Bookmark

>>> client = Client()

>>> response = client.get('/bookmarks/')
>>> response.status_code
200

>>> bookmark = Bookmark(url='http://www.djangobook.com', description='Django book', extended='Great resource!')
>>> bookmark.save()
>>> response = client.get(bookmark.get_absolute_url())
>>> response.status_code
200
"""