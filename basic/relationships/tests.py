"""
>>> from django.test import Client
>>> from django.core import management
>>> from django.core.urlresolvers import reverse
>>> from django.contrib.auth.models import User
>>> from basic.relationships.models import *

>>> c = Client()

>>> management.call_command('loaddata', 'users.json', verbosity=0)

>>> c.login(username='nathanb', password='n')
True

>>> nathan = User.objects.get(username='nathanb')
>>> laura = User.objects.get(username='laurah')

>>> response = c.get(reverse('relationship_follow', kwargs={'to_user_id':laura.id}))
>>> response.status_code
200

>>> response = c.post(reverse('relationship_follow', kwargs={'to_user_id':laura.id}))
>>> response.status_code
200

"""