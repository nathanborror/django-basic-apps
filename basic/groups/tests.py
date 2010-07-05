from django.test import TestCase
from django.core import management
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from basic.groups.models import *


class GroupTestCase(TestCase):
    fixtures = ['groups.json', 'users.json']

    def setUp(self):
        self.user1 = User.objects.get(username='nathanb')
        self.user2 = User.objects.get(username='laurah')

        self.group = Group.objects.get(pk=1)
        self.topic = GroupTopic.objects.get(pk=1)
        self.message = GroupMessage.objects.get(pk=1)
        self.page = GroupPage.objects.get(pk=1)

        self.client.login(username=self.user1.username, password='n')

    def test_groups(self):
        group_args = [self.group.slug]

        response = self.client.get(reverse('groups:groups'))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('groups:group', args=group_args))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('groups:create'))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('groups:create'), {
            'title': 'My new group',
            'slug': 'my-new-group'
        })
        self.assertEqual(response.status_code, 302)

        group = Group.objects.get(pk=2)

        response = self.client.get(reverse('groups:edit', args=group_args))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('groups:edit', args=[group.slug]), {
            'title': 'My really new group',
            'slug': 'my-new-group'
        })
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse('groups:remove', args=[group.slug]))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('groups:remove', args=[group.slug]))
        self.assertEqual(response.status_code, 302)

    def test_group_membership(self):
        response = self.client.get(reverse('groups:join', args=[self.group.slug]))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('groups:members', args=[self.group.slug]))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('groups:invite', args=[self.group.slug]))
        self.assertEqual(response.status_code, 200)

    def test_pages(self):
        page_args = [self.group.slug, self.page.slug]

        response = self.client.get(reverse('groups:pages', args=[self.group.slug]))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('groups:page_create', args=[self.group.slug]))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('groups:page_create', args=[self.group.slug]), {
            'title': 'Contact us',
            'slug': 'contact',
            'body': 'Lorem ipsum dolor sit amet, consectetur adipisicing elit.'
        })
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse('groups:page', args=page_args))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('groups:page_edit', args=page_args))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('groups:page_edit', args=page_args), {
            'title': 'About our group',
            'slug': 'about'
        })
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse('groups:page_remove', args=page_args))
        self.assertEqual(response.status_code, 200)

    def test_topics(self):
        response = self.client.get(reverse('groups:topics', args=[self.group.slug]))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('groups:topic_create', args=[self.group.slug]))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(self.topic.get_absolute_url())
        self.assertEqual(response.status_code, 200)

        response = self.client.get(self.topic.get_edit_url())
        self.assertEqual(response.status_code, 200)

        response = self.client.get(self.topic.get_remove_url())
        self.assertEqual(response.status_code, 200)

    def test_messages(self):
        response = self.client.get(reverse('groups:message_create', args=[self.group.slug, self.topic.pk]))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(self.message.get_absolute_url())
        self.assertEqual(response.status_code, 200)

        response = self.client.get(self.message.get_edit_url())
        self.assertEqual(response.status_code, 200)

        response = self.client.get(self.message.get_remove_url())
        self.assertEqual(response.status_code, 200)
