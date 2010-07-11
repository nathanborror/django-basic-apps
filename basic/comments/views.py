import datetime

from django.conf import settings
from django.shortcuts import get_object_or_404
from django.contrib.comments.models import Comment

from basic.comments.forms import CommentForm
from basic.tools.shortcuts import render, redirect


DELTA = datetime.datetime.now() - datetime.timedelta(
            minutes=getattr(settings, 'COMMENT_ALTERATION_TIME_LIMIT', 15))


def comment_edit(request, object_id, template_name='comments/edit.html'):
    comment = get_object_or_404(Comment, pk=object_id, user=request.user)

    if DELTA > comment.submit_date:
         return comment_error(request)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect(request, comment.content_object)
    else:
        form = CommentForm(instance=comment)
    return render(request, template_name, {
        'form': form,
        'comment': comment,
    })


def comment_remove(request, object_id, template_name='comments/delete.html'):
    comment = get_object_or_404(Comment, pk=object_id, user=request.user)

    if DELTA > comment.submit_date:
         return comment_error(request)

    if request.method == 'POST':
        comment.delete()
        return redirect(request, comment.content_object)
    return render(request, template_name, {'comment': comment})


def comment_error(request, error_message='You can not change this comment.',
        template_name='comments/error.html'):
    return render(request, template_name, {'error_message': error_message})
