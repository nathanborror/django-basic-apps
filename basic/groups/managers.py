from django.db.models import Manager
import datetime


class GroupMessageManager(Manager):
    """Returns messages that are flagged as active."""

    def get_query_set(self):
        return super(GroupMessageManager, self).get_query_set().filter(is_active=True)


class GroupMemberManager(Manager):
    """Returns memebers that belong to a group"""

    def is_member(self, group, user):
        if user.is_anonymous():
            return False
        if self.filter(group=group, user=user).count() > 0:
            return True
        return False

    def is_owner(self, group, user):
        if user.is_anonymous():
            return False
        if self.filter(group=group, user=user, status=0).count() > 0:
            return True
        return False

    def is_moderator(self, group, user):
        if user.is_anonymous():
            return False
        if self.filter(group=group, user=user, status=1).count() > 0:
            return True
        return False