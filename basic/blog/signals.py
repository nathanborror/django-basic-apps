from django.core.cache import cache
from basic.blog.models import Settings
from sugar.cache.utils import create_cache_key

def invalidate_settings_cache(sender=None, instance=None, isnew=False, **kwargs):

    if isnew:
        return

    site_id = instance.site.id
    key = create_cache_key(Settings, field='site__id', field_value=site_id)
    #invalidate cache, set to None for 5 seconds to safegaurd
    #against race condition; concept borrowed from mmalone's django-caching
    cache.set(key, None, 5)
