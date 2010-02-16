from django import forms
from django.contrib.auth.models import User

from basic.messages.models import Message


class MessageForm(forms.ModelForm):
    to_user = forms.CharField()

    class Meta:
        model = Message
        exclude = ('to_status', 'from_status', 'from_user', 'object_id', 'content_type')