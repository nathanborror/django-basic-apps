from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.sites.models import Site


INVITATION_ALLOTMENT = getattr(settings, 'INVITATION_ALLOTMENT', 5)

INVITATION_STATUS_SENT = 0
INVITATION_STATUS_ACCEPTED = 1
INVITATION_STATUS_DECLINED = 2
INVITATION_STATUS_CHOICES = (
    (INVITATION_STATUS_SENT, 'Sent'),
    (INVITATION_STATUS_DECLINED, 'Accepted'),
    (INVITATION_STATUS_DECLINED, 'Declined'),
)


class Invitation(models.Model):
    """ Invitation model """
    from_user = models.ForeignKey(User)
    name = models.CharField(blank=True, max_length=100)
    email = models.EmailField()
    message = models.TextField(blank=True)
    status = models.PositiveSmallIntegerField(choices=INVITATION_STATUS_CHOICES, default=0)
    site = models.ForeignKey(Site, default=settings.SITE_ID)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '<Invite>'

    @models.permalink
    def get_absolute_url(self):
        return ('registration_register', [])


class InvitationAllotment(models.Model):
    """ InvitationAllotment model """
    user = models.OneToOneField(User)
    amount = models.IntegerField(default=INVITATION_ALLOTMENT)
    site = models.ForeignKey(Site, default=settings.SITE_ID)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '<Invitation Allotment>'

    def decrement(self, amount=1):
        self.amount = self.amount - amount
        self.save()
