from basic.blog.models import Settings
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

    blog_settings = Settings.get_current()

    return {
        'BLOG_SETTINGS': blog_settings,
    }