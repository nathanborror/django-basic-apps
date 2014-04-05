from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.cache import cache
from django.conf import settings


RELATIONSHIP_CACHE = getattr(settings, 'RELATIONSHIP_CACHE', 60*60*24*7)
RELATIONSHIP_CACHE_KEYS = {
    'FRIENDS': 'friends',
    'FOLLOWERS': 'followers',
    'BLOCKERS': 'blockers',
    'FANS': 'fans'
}


class RelationshipManager(models.Manager):
    def _set_cache(self, user, user_list, relationship_type, flat=False, flat_attr='to_user'):
        cache_key = 'user_%s_%s' % (user.pk, relationship_type)
        if flat:
            cache_key = cache_key+'_flat'
            user_list = user_list.values_list(flat_attr, flat=True)
        if not cache.get(cache_key):
            cache.set(cache_key, list(user_list), RELATIONSHIP_CACHE)
        return user_list

    def get_blockers_for_user(self, user, flat=False):
        """Returns list of people blocking user."""
        user_list = self.filter(to_user=user, is_blocked=True)
        return self._set_cache(user, user_list, RELATIONSHIP_CACHE_KEYS['BLOCKERS'], flat=flat, flat_attr='from_user')

    def get_friends_for_user(self, user, flat=False):
        """Returns people user is following sans people blocking user."""
        blocked_id_list = self.get_blockers_for_user(user, flat=True)
        user_list = self.filter(from_user=user, is_blocked=False).exclude(to_user__in=blocked_id_list)
        return self._set_cache(user, user_list, RELATIONSHIP_CACHE_KEYS['FRIENDS'], flat=flat)

    def get_followers_for_user(self, user, flat=False):
        """Returns people following user."""
        user_list = self.filter(to_user=user, is_blocked=False)
        return self._set_cache(user, user_list, RELATIONSHIP_CACHE_KEYS['FOLLOWERS'], flat=flat, flat_attr='from_user')

    def get_fans_for_user(self, user, flat=False):
        """Returns people following user but user isn't following."""
        friend_id_list = self.get_friends_for_user(user, flat=True)
        user_list = self.filter(to_user=user, is_blocked=False).exclude(from_user__in=friend_id_list)
        return self._set_cache(user, user_list, RELATIONSHIP_CACHE_KEYS['FANS'], flat=flat, flat_attr='from_user')

    def get_relationship(self, from_user, to_user):
        try:
            relationship = self.get(from_user=from_user, to_user=to_user)
        except:
            return None
        return relationship

    def blocking(self, from_user, to_user):
        """Returns True if from_user is blocking to_user."""
        try:
            relationship = self.get(from_user=from_user, to_user=to_user)
            if relationship.is_blocked:
                return True
        except:
            return False
        return False

class Relationship(models.Model):
    """Relationship model"""
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='from_users')
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='to_users')
    created = models.DateTimeField(auto_now_add=True)
    is_blocked = models.BooleanField(default=False)
    objects = RelationshipManager()

    class Meta:
        unique_together = (('from_user', 'to_user'),)
        verbose_name = _('relationship')
        verbose_name_plural = _('relationships')
        db_table = 'relationships'

    def __unicode__(self):
        if self.is_blocked:
            return u'%s is blocking %s' % (self.from_user, self.to_user)
        return u'%s is connected to %s' % (self.from_user, self.to_user)

    def save(self, *args, **kwargs):
        self._delete_cache_keys()
        super(Relationship, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self._delete_cache_keys()
        super(Relationship, self).delete(*args, **kwargs)

    def _delete_cache_keys(self):
        for key in RELATIONSHIP_CACHE_KEYS:
            cache.delete('user_%s_%s' % (self.from_user.pk, RELATIONSHIP_CACHE_KEYS[key]))
            cache.delete('user_%s_%s_flat' % (self.from_user.pk, RELATIONSHIP_CACHE_KEYS[key]))