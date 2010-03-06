from django.test import TestCase
from django.core import management
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from basic.groups.models import *


class GroupTestCase(TestCase):
    fixtures = ['groups.json']

    def setUp(self):
        self.user = User.objects.get(username='nathanb')
        self.slug = 'infinite-summer'

    def test_anonymous_join(self):
        response = self.client.get(reverse('group_join', kwargs={'slug': self.slug}))
        self.assertEqual(response.status_code, 302)

    def test_anonymous_members(self):
        response = self.client.get(reverse('group_members', kwargs={'slug': self.slug}))
        self.assertEqual(response.status_code, 200)

    def test_anonymous_groups(self):
        kwargs = {'slug': self.slug}

        response = self.client.get(reverse('groups'))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('group', kwargs=kwargs))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('group_edit', kwargs=kwargs))
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse('group_remove', kwargs=kwargs))
        self.assertEqual(response.status_code, 302)

    def test_anonymous_topics(self):
        kwargs = {'slug': self.slug}

        response = self.client.get(reverse('group_topics', kwargs=kwargs))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('group_topic_create', kwargs=kwargs))
        self.assertEqual(response.status_code, 302)

        kwargs['topic_id'] = 1

        response = self.client.get(reverse('group_topic', kwargs=kwargs))
        self.assertEqual(response.status_code, 200)

        kwargs = {
            'slug': 'infinite-summer',
            'topic_id': 1
        }

        response = self.client.get(reverse('group_topic_edit', kwargs=kwargs))
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse('group_topic_remove', kwargs=kwargs))
        self.assertEqual(response.status_code, 302)

    def test_anonymous_messages(self):
        kwargs = {
            'slug': self.slug,
            'topic_id': 1
        }

        response = self.client.get(reverse('group_message_create', kwargs=kwargs))
        self.assertEqual(response.status_code, 302)

        kwargs['message_id'] = 1

        response = self.client.get(reverse('group_topic_message', kwargs=kwargs))
        self.assertEqual(response.status_code, 200)

        kwargs = {
            'slug': self.slug,
            'message_id': 1
        }

        response = self.client.get(reverse('group_message_edit', kwargs=kwargs))
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse('group_message_remove', kwargs=kwargs))
        self.assertEqual(response.status_code, 302)

    def test_groups(self):
        self.client.login(username=self.user.username, password='n')

        response = self.client.get(reverse('group', kwargs={'slug': self.slug}))
        self.assertEqual(response.status_code, 200)

        kwargs = {
            'title': 'My new gorup',
            'slug': 'my-new-group',
            'invite_only': 0
        }
        response = self.client.post(reverse('group_create'), kwargs)
        self.assertEqual(response.status_code, 200)

    def test_join(self):
        self.client.login(username=self.user.username, password='n')

        response = self.client.get(reverse('group_join', kwargs={'slug': self.slug}))
        self.assertEqual(response.status_code, 200)

    # TEST GROUP EDIT/DELETE
    # TEST TOPICS
    # TEST MESSAGES