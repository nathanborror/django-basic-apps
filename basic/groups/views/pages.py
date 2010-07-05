from django.shortcuts import get_object_or_404

from basic.groups.decorators import *
from basic.groups.models import *
from basic.groups.forms import *
from basic.tools.shortcuts import render, redirect


def page_list(request, slug, template_name='groups/pages/page_list.html'):
    """
    Returns a list of pages for a group.

    Templates: ``groups/pages/page_list.html``
    Context:
        group
            Group object
        page_list
            List of GroupPage objects
    """
    group = get_object_or_404(Group, slug=slug)
    return render(request, template_name, {
        'group': group,
        'page_list': group.pages.all()
    })


def page_detail(request, slug, page_slug,
        template_name='groups/pages/page_detail.html'):
    """
    Returns a group page.

    Templates: ``groups/pages/page_detail.html``
    Context:
        group
            Group object
        page
            GroupPage object
    """
    group = get_object_or_404(Group, slug=slug)
    page = get_object_or_404(GroupPage, group=group, slug=page_slug)
    return render(request, template_name, {
        'group': group,
        'page': page
    })


@ownership_required
def page_create(request, slug, template_name='groups/pages/page_form.html'):
    """
    Creates a group page.

    Templates: ``groups/pages/page_form.html``
    Context:
        group
            Group object
        form
            PageForm object
    """
    group = get_object_or_404(Group, slug=slug)
    form = GroupPageForm(initial={'group': group})

    if request.method == 'POST':
        form = GroupPageForm(request.POST)
        if form.is_valid():
            page = form.save(commit=False)
            page.group = group
            page.save()
            return redirect(request, page)

    return render(request, template_name, {
        'group': group,
        'form': form
    })


@ownership_required
def page_edit(request, slug, page_slug,
        template_name='groups/pages/page_form.html'):
    group = get_object_or_404(Group, slug=slug)
    page = get_object_or_404(GroupPage, group=group, slug=page_slug)
    form = GroupPageForm(instance=page)

    if request.method == 'POST':
        form = GroupPageForm(request.POST, instance=page)
        if form.is_valid():
            page = form.save()
            return redirect(request, page)

    return render(request, template_name, {
        'group': group,
        'page': page,
        'form': form
    })


@ownership_required
def page_remove(request, slug, page_slug,
        template_name='groups/pages/page_remove_confirm.html'):
    group = get_object_or_404(Group, slug=slug)
    page = get_object_or_404(GroupPage, group=group, slug=page_slug)

    if request.method == 'POST':
        page.delete()
        return redirect(request, group)

    return render(request, template_name, {
        'group': group,
        'page': page
    })
