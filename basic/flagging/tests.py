from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

from basic.flagging.models import *


class FlaggingTestCase(TestCase):
    fixtures = ['flagging.json']

    def setUp(self):
        self.user = User.objects.get(username='nathanb')
        self.ct = ContentType.objects.get_for_model(self.user)
        self.flag_type = FlagType.objects.create(content_type=self.ct, title='Test flagging', slug='test-flagging')

    def test_flagging(self):
        self.client.login(username=self.user.username, password='n')

        friend = User.objects.get(username='laurah')
        flag_type = FlagType.objects.create(content_type=self.ct)
        kwargs = {
            'flag_type_slug': self.flag_type.slug,
            'object_id': friend.pk
        }
        response = self.client.get(reverse('flag', kwargs=kwargs))
        self.assertEqual(response.status_code, 200)

    def test_unflagging(self):
        self.client.login(username=self.user.username, password='n')

        friend = User.objects.get(username='laurah')
        flag_type = FlagType.objects.create(content_type=self.ct)
        kwargs = {
            'flag_type_slug': self.flag_type.slug,
            'object_id': friend.pk
        }
        response = self.client.get(reverse('unflag', kwargs=kwargs))
        self.assertEqual(response.status_code, 200)