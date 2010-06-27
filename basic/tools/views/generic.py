from django.db.models import Q
from django.utils import simplejson as json
from django.http import HttpResponse


def auto_complete(request, queryset, fields=None):
    """
    Returns a JSON list to be used with the AutoCompleteWidget javascript.

    Example:

        url(r'^autocomplete/$',
            view='basic.tools.views.generic.auto_complete',
            kwargs={
                'queryset': Author.objects.all()
                'fields': ('first_name__icontains', 'last_name__icontains')
            }
        )

    """
    object_list = []
    limit = request.GET.get('limit', 10)
    query = request.GET.get('q', '')
    if fields:
        q_objects = []
        for field in fields:
            kwargs = {field: query}
            q_objects.append(Q(**kwargs))
        args = reduce(lambda q1, q2: q1 | q2, q_objects)
        queryset = queryset.filter(args)

    for obj in queryset[:limit]:
        object_list.append({'text': obj.__unicode__(), 'id': obj.pk})
    return HttpResponse(json.dumps(object_list), mimetype='application/json')