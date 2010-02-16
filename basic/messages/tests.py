from django.test import TestCase
from django.core import management
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from basic.messages.models import *


class SocialTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.get(username='nathan')

    def test_private(self):
        self.client.login(username=self.user.username, password='n')

        response = self.client.get(reverse('message_list'))
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get(reverse('message_create'))
        self.assertEqual(response.status_code, 200)

"""
>>> shawn = User.objects.get(username='shawn')

>>> request = c.post(reverse('message_compose'), {'to_user': shawn.id, 'subject': 'Lorem ipsum', 'message': 'Lorem ipsum dolor sit amet'})
>>> request.status_code
302

>>> request = c.get(reverse('messages'))
>>> request.status_code
200

>>> request = c.get(reverse('message', args=('sent', 1)))
>>> request.status_code
200

>>> request = c.get(reverse('messages_group', args=('inbox',)))
>>> request.status_code
200

>>> request = c.get(reverse('messages_group', args=('sent',)))
>>> request.status_code
200

>>> request = c.post(reverse('message_delete'), {'object_id': 1})
>>> request.status_code
302
"""