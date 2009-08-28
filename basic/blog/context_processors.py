from django.conf import settings
from basic.blog.models import Category
from django.core.cache import cache
from basic.blog.models import Settings
from basic.elsewhere.models import SocialNetworkProfile
from sugar.cache.utils import create_cache_key

def blog_settings(request):
    """
    Adds settings information to the context.
    
    To employ, add the basic_settings method reference to your project 
    settings TEMPLATE_CONTEXT_PROCESSORS.
    
    Example:
        TEMPLATE_CONTEXT_PROCESSORS = (
            ...
            "basic.blog.context_processors.blog_settings",
        )
    """
    
    site_id = settings.SITE_ID   
    key = create_cache_key(Settings, field_name='pk', field_value=site_id)
    blog_settings = cache.get(key, None)
    if blog_settings is None:
        blog_settings = Settings.get_current()
        cache.set(key, blog_settings)
        
    return {
        'BLOG_SETTINGS': blog_settings,
    }