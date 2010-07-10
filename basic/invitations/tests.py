from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from basic.invitations.models import *


class InvitationTestCase(TestCase):
    fixtures = ['users.json', 'invitations.json']

    def setUp(self):
        self.user = User.objects.get(username='nathanb')
        self.client.login(username=self.user.username, password='n')

    def test_invitations(self):
        response = self.client.get(reverse('invitations:create'))
        self.assertEqual(response.status_code, 200)

        post = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'message': 'Test message',
        }
        response = self.client.post(reverse('invitations:create'), post)
        self.assertEqual(response.status_code, 200)

        invitation = Invitation.objects.get(pk=1)

        response = self.client.get(invitation.get_absolute_url())
        self.assertEqual(response.status_code, 200)
