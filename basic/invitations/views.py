from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.sites.models import Site

from basic.invitations.models import Invitation, InvitationAllotment
from basic.invitations.forms import InvitationForm
from basic.tools.shortcuts import render, redirect

from registration.views import register


@login_required
def invitation_create(request, template_name='invitations/invitation_form.html',
        success_template_name='invitations/invitation_success.html'):
    """
    Returns a form for a user to send an invitation.

    Templates:
        ``invitations/invitation_form.html``
        ``invitations/invitation_success.html``

    Context:
        form
            InvitationForm object
    """
    try:
        allotment = request.user.invitation_allotment
        if allotment.amount == 0:
            return invitation_error(request)
    except InvitationAllotment.DoesNotExist:
        return invitation_error(request)

    if request.method == 'POST':
        form = InvitationForm(request.POST)
        if form.is_valid():
            invitation = form.save(commit=False)
            invitation.token = Invitation.objects.create_token(invitation.email)
            invitation.from_user = request.user
            invitation.save()

            # Reduce user's invitation allotment
            allotment.decrement(1)

            # Send invitation email
            send_invitation_email(invitation)
            return render(request, success_template_name)
    else:
        form = InvitationForm()

    return render(request, template_name, {'form': form})


@login_required
def invitation_error(request, error_message='You do not have any invitations at this time.',
        template_name='invitations/invitation_error.html'):
    """
    Returns an error template.

    Template: ``invitations/invitation_error.html``

    Context:
        error_message
            String containing the error message.
    """
    return render(request, template_name, {
        'error_message': error_message
    })


def invitation_detail(request, token):
    """
    Returns a sign up form via the django-registration app if the URL is valid.
    """
    invitation = Invitation.objects.get_invitation(token)
    if not invitation:
        return invitation_error(request, "This invitation is no longer valid.")

    backend = getattr(settings, 'REGISTRATION_BACKEND', 'registration.backends.default.DefaultBackend')
    return register(request, backend)


def send_invitation_email(invitation):
    site = Site.objects.get_current()
    context = {'invitation': invitation, 'site': site}
    subject = render_to_string('invitations/invitation_subject.txt', context)
    message = render_to_string('invitations/invitation_message.txt', context)

    INVITATION_FROM_EMAIL = getattr(settings, 'INVITATION_FROM_EMAIL', '')

    email = EmailMessage(subject, message, INVITATION_FROM_EMAIL, ['%s' % invitation.email])
    email.send(fail_silently=True)
