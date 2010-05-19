from django import forms
from django.contrib.auth.models import User

from basic.messages.models import Message


class MessageForm(forms.ModelForm):
    to_user = forms.CharField()

    class Meta:
        model = Message
        exclude = ('to_status', 'from_status', 'from_user', 'object_id', 'content_type')

    def clean_to_user(self):
        if self.cleaned_data['to_user']:
            try:
                user = User.objects.get(username=self.cleaned_data['to_user'])
                self.cleaned_data['to_user'] = user
                return self.cleaned_data['to_user']
            except User.DoesNotExist:
                pass
        raise forms.ValidationError(u'There are no users with this username.')