from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import Http404, HttpResponseRedirect
from django.views.generic import list_detail
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from basic.profiles.models import *
from basic.profiles.forms import *

from django.core.exceptions import ObjectDoesNotExist

def get_or_create_profile(user):
    try:
        #Update by Leon de Almeida:
        #   enable profiles to be created automatically if they don't exist
        #profile = user.get_profile()
        profile = Profile.objects.get(user=user)
    except ObjectDoesNotExist:
        profile = Profile(user=user)
        profile.save()
        
    return profile

def profile_list(request):
    return list_detail.object_list(
        request,
        queryset=Profile.objects.all(),
        paginate_by=20,
    )
profile_list.__doc__ = list_detail.object_list.__doc__


def profile_detail(request, username):
    try:
        user = User.objects.get(username__iexact=username)
    except User.DoesNotExist:
        raise Http404
    
    #Update by Leon de Almeida:
    #   enable profiles to be created automatically if they don't exist
    #profile = Profile.objects.get(user=user)
    profile = get_or_create_profile(user=user)
    context = { 'object':profile }
    return render_to_response('profiles/profile_detail.html', context, context_instance=RequestContext(request))


@login_required
def profile_edit(request, template_name='profiles/profile_form.html'):
    """Edit profile."""

    if request.POST:
        #Update by Leon de Almeida:
        #   enable profiles to be created automatically if they don't exist
        #profile = Profile.objects.get(user=request.user)
        profile = get_or_create_profile(user=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        user_form = UserForm(request.POST, instance=request.user)
        service_formset = ServiceFormSet(request.POST, instance=profile)
        link_formset = LinkFormSet(request.POST, instance=profile)

        if profile_form.is_valid() and user_form.is_valid() and service_formset.is_valid() and link_formset.is_valid():
            profile_form.save()
            user_form.save()
            service_formset.save()
            link_formset.save()
            return HttpResponseRedirect(reverse('profile_detail', kwargs={'username': request.user.username}))
        else:
            context = {
                'profile_form': profile_form,
                'user_form': user_form,
                'service_formset': service_formset,
                'link_formset': link_formset
            }
    else:
        #Update by Leon de Almeida:
        #   enable profiles to be created automatically if they don't exist
        #profile = Profile.objects.get(user=request.user)
        profile = get_or_create_profile(user=request.user)
        service_formset = ServiceFormSet(instance=profile)
        link_formset = LinkFormSet(instance=profile)
        context = {
            'profile_form': ProfileForm(instance=profile),
            'user_form': UserForm(instance=request.user),
            'service_formset': service_formset,
            'link_formset': link_formset
        }
    return render_to_response(template_name, context, context_instance=RequestContext(request))