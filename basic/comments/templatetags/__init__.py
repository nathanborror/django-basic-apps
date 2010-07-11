from django.contrib.comments.models import Comment
from django.contrib.comments.forms import CommentForm


def get_model():
    return Comment


def get_form():
    return CommentForm