from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from basic.messages.models import *


class MessageTestCase(TestCase):
    fixtures = ['users.json']
    
    def setUp(self):
        self.user1 = User.objects.get(username='nathanb')
        self.user2 = User.objects.get(username='laurah')
        
    def test_messages(self):
        self.client.login(username=self.user1.username, password='n')
        
        response = self.client.get(reverse('messages:messages'))
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get(reverse('messages:create'))
        self.assertEqual(response.status_code, 200)
        
        post = {
            'to_user': 'laurah',
            'subject': 'Test subject',
            'message': 'Test message',
        }
        response = self.client.post(reverse('messages:create'), post)
        self.assertEqual(response.status_code, 302)
        
        response = self.client.get(reverse('messages:messages', kwargs={'mailbox': 'sent'}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context[0]['message_list']), '[<Message: Message from nathanb>]')
        self.assertEqual(str(response.context[0]['mailbox']), 'sent')
        
        self.client.login(username=self.user2.username, password='l')
        
        response = self.client.get(reverse('messages:messages'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context[0]['message_list']), '[<Message: Message from nathanb>]')
        self.assertEqual(str(response.context[0]['mailbox']), 'archive')
        
        message = response.context[0]['message_list'][0]
        response = self.client.get(message.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get(reverse('messages:reply', kwargs={'object_id': message.pk}))
        self.assertEqual(response.status_code, 200)
