from django.db import models
from django.utils.translation import ugettext_lazy as _

class SocialNetworkProfile(models.Model):
	'''
	Represents a person's social networks they belong to.
	
	A minimalist version of django-elsewhwere.
	'''
	
	name = models.CharField(_('name'), max_length=100, blank=False, null=True, 
							help_text=_('The name displayed in templates.'))
	url = models.URLField(_('url'), verify_exists=False, help_text=_('The your for your profile'))
	sort_order = models.PositiveIntegerField(_('sort order'), default=0)
	description = models.TextField(_('description'), blank=True, null=True, 
							help_text=_('Description of the bookmark. Raw HTML is allowed.'))
	category = models.ForeignKey('Category')
	
	class Meta:
		verbose_name = _('social network profile')
		verbose_name_plural = _('social network profile')
		ordering = ('sort_order', 'name', )
	
	def __unicode__(self):
		return self.url

	def get_absolute_url(self):
		return self.url

class Category(models.Model):
    '''
    Represents a category for organizing Profiles.
    
    Example: Projects, Social, etc.
    
    '''
    
    title = models.CharField(_('title'), max_length=100, blank=False, null=True, unique=True)
    sort_order = models.PositiveIntegerField(_('sort order'), default=0)

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        ordering = ('sort_order', 'title', )

    def __unicode__(self):
        return self.title
        
