from django import forms
from django.contrib.auth.models import User

from basic.groups.models import *


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        exclude = ('creator', 'is_active')


class GroupTopicForm(forms.ModelForm):
    class Meta:
        model = GroupTopic
        exclude = ('group', 'user', 'is_active')


class GroupMessageForm(forms.ModelForm):
    class Meta:
        model = GroupMessage
        exclude = ('topic', 'user', 'is_active')


class GroupInviteForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput)
    group = forms.ModelChoiceField(queryset=Group.objects.all(), widget=forms.HiddenInput)
    name = forms.CharField()
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)


class GroupPageForm(forms.ModelForm):
    class Meta:
        model = GroupPage
        exclude = ('group',)