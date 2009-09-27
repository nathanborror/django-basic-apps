from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class RelationshipManager(models.Manager):
    def relationships_for_user(self, user):
        """
        Relationships for user

        Returns a list of friends, people you are following, and followers,
        people that are following you but you are not following.
        """
        friend_list = self.filter(from_user=user)
        follower_list = self.filter(to_user=user)

        friend_id_list = self.filter(from_user=user).values_list('to_user', flat=True)
        fan_list = follower_list & self.exclude(from_user__in=friend_id_list)

        relationships = {
            'friends': friend_list,
            'followers': follower_list,
            'fans': fan_list
        }

        return relationships

    def is_following(self, you, them):
        """Answers the question, am I following you?"""
        if self.filter(from_user=you, to_user=them).count() > 0:
            return True
        return False

    def is_follower(self, you, them):
        """Answers the question, are you following me?"""
        if self.filter(from_user=them, to_user=you).count() > 0:
            return True
        return False


class Relationship(models.Model):
    """ Relationship model """
    from_user       = models.ForeignKey(User, related_name='from_users')
    to_user         = models.ForeignKey(User, related_name='to_users')
    created         = models.DateTimeField(auto_now_add=True)
    objects         = RelationshipManager()

    class Meta:
        unique_together = (('from_user', 'to_user'),)
        verbose_name = _('relationship')
        verbose_name_plural = _('relationships')
        db_table = 'relationships'

    def __unicode__(self):
        return u'%s is connected to %s' % (self.from_user, self.to_user)