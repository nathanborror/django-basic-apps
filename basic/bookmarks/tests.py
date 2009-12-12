"""
>>> from django.test import Client
>>> from basic.bookmarks.models import Bookmark

>>> client = Client()

>>> response = client.get('/bookmarks/')
>>> response.status_code
200

>>> bookmark = Bookmark(url='http://www.google.com', description='Django book', extended='Great resource!')
>>> bookmark.save()

"""