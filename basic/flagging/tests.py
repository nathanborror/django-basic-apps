from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

from basic.flagging.models import *


class FlaggingTestCase(TestCase):
    fixtures = ['flagging.json']

    def setUp(self):
        self.user = User.objects.get(username='nathanb')
        self.ctype = ContentType.objects.get_for_model(self.user)
        self.flag_type = FlagType.objects.create(title='Test flagging', slug='test-flagging')
        self.friend = User.objects.get(username='laurah')

    def test_flagging(self):
        self.client.login(username=self.user.username, password='n')

        kwargs = {
            'slug': self.flag_type.slug,
            'app_label': self.ctype.app_label,
            'model': self.ctype.model,
            'object_id': self.friend.pk,
        }
        response = self.client.get(reverse('flag', kwargs=kwargs))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('flag', kwargs=kwargs))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('unflag', kwargs=kwargs))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('unflag', kwargs=kwargs))
        #self.assertEqual(response.status_code, 200)

        kwargs = {
            'username': 'nathanb',
            'slug': 'test-flagging'
        }
        response = self.client.get(reverse('user_flags', kwargs=kwargs))
        self.assertEqual(response.status_code, 200)