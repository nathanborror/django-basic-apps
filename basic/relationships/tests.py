from django.test import TestCase, override_settings
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from basic.relationships.models import *


class RelationshipTestCase(TestCase):

    @override_settings(AUTH_USER_MODEL='auth.User')
    def setUp(self):
        self.user1 = User.objects.create_user('nathanb', email='nathanb@example.com', password='n')
        self.user2 = User.objects.create_user('laurah', email='laurah@example.com', password='l')
        
    @override_settings(AUTH_USER_MODEL='auth.User')
    def test_follow(self):
        self.client.login(username=self.user1.username, password='n')

        kwargs = {'username': self.user2.username}

        # GET request displays confirmation form
        response = self.client.get(reverse('relationship_follow', kwargs=kwargs))
        self.assertEqual(response.status_code, 200)

        # POST request saves relationship
        response = self.client.post(reverse('relationship_follow', kwargs=kwargs))
        self.assertEqual(response.status_code, 200)

        friends = Relationship.objects.get_friends_for_user(self.user1)
        self.assertEqual(len(friends), 1)

        followers = Relationship.objects.get_followers_for_user(self.user2)
        self.assertEqual(len(followers), 1)

        fans = Relationship.objects.get_fans_for_user(self.user2)
        self.assertEqual(len(fans), 1)
        
    @override_settings(AUTH_USER_MODEL='auth.User')
    def test_block(self):
        self.client.login(username=self.user1.username, password='n')

        kwargs = {'username': self.user2.username}

        # GET request displays confirmation form
        response = self.client.get(reverse('relationship_block', kwargs=kwargs))
        self.assertEqual(response.status_code, 200)

        # POST request saves block
        response = self.client.post(reverse('relationship_block', kwargs=kwargs))
        self.assertEqual(response.status_code, 200)

        blocked = Relationship.objects.get_blockers_for_user(self.user2)
        self.assertEqual(len(blocked), 1)

        # Login as different user
        self.client.login(username=self.user2.username, password='l')

        # POST request saves relationship
        response = self.client.post(reverse('relationship_follow', kwargs={'username': self.user1.username}))
        self.assertEqual(response.status_code, 200)

        friends = Relationship.objects.get_friends_for_user(self.user2)
        self.assertEqual(len(friends), 0)
        
    @override_settings(AUTH_USER_MODEL='auth.User')
    def test_following(self):
        kwargs = {'username': self.user1.username}
        
        # Test with no relations.
        response = self.client.get(reverse('relationship_following', kwargs=kwargs))
        self.assertEqual(response.status_code, 200)
        self.assertEqual([following.id for following in response.context['page'].object_list], [])
        
        # Setup a relationship.
        Relationship.objects.create(from_user=self.user1, to_user=self.user2)
        
        # Test the relationship.
        response = self.client.get(reverse('relationship_following', kwargs=kwargs))
        self.assertEqual(response.status_code, 200)
        self.assertEqual([following.id for following in response.context['page'].object_list], [self.user2.pk])
        
    @override_settings(AUTH_USER_MODEL='auth.User')
    def test_followers(self):
        kwargs = {'username': self.user2.username}
        
        # Test with no relations.
        response = self.client.get(reverse('relationship_followers', kwargs=kwargs))
        self.assertEqual(response.status_code, 200)
        self.assertEqual([following.id for following in response.context['page'].object_list], [])
        
        # Setup a relationship.
        Relationship.objects.create(from_user=self.user1, to_user=self.user2)
        
        # Test the relationship.
        response = self.client.get(reverse('relationship_followers', kwargs=kwargs))
        self.assertEqual(response.status_code, 200)
        self.assertEqual([following.id for following in response.context['page'].object_list], [self.user1.pk])
