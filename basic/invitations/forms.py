from django import forms
from django.contrib.auth.models import User

from basic.invitations.models import Invitation


class InvitationForm(forms.ModelForm):
    class Meta:
        model = Invitation
        exclude = ('status', 'from_user', 'site', 'token')
