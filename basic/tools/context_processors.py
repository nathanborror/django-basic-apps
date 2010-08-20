from datetime import datetime

from django.conf import settings
from django.contrib.sites.models import Site


def site(request):
    """
    Adds the current site to the context.
    """
    return {'site': Site.objects.get(id=settings.SITE_ID)}


def now(request):
    """
    Add current datetime to template context.
    """
    return {'now': datetime.now()}
