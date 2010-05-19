from django.test import TestCase
from django.core import management
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from basic.messages.models import *


class MessageTestCase(TestCase):
    fixtures = ['users.json']

    def setUp(self):
        self.user = User.objects.get(username='nathanb')

    def test_private(self):
        self.client.login(username=self.user.username, password='n')

        response = self.client.get(reverse('messages'))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('message_create'))
        self.assertEqual(response.status_code, 200)
