from basic.blog.models import Settings
from basic.blog.signals import invalidate_settings_cache
from django.db.models import signals

signals.post_save.connect(invalidate_settings_cache, Settings, True)
