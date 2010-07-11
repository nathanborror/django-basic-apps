from django.forms import ModelForm
from django.contrib.comments.models import Comment


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        exclude = ('content_type', 'object_pk', 'site', 'user', 'is_public',
            'user_name', 'user_email', 'user_url', 'submit_date', 'ip_address',
            'is_removed',)