from django.forms.widgets import Widget, HiddenInput, TextInput
from django.utils.safestring import mark_safe


class AutoCompleteWidget(Widget):
    """
    Widget that presents an <input> field that can be used to search for
    objects instead of a giant <select> field

    You will need to include jQuery Autocomplete which can be found here:
    http://docs.jquery.com/Plugins/Autocomplete

    Include media:

        basic/tools/media/stylesheets/autocomplete.css
        basic/tools/media/javascript/autocomplete.js

    Example form:

        from basic.tools.forms import fields

        class BookForm(forms.Form):
            authors = forms.ModelMultipleChoiceField(
                queryset=Author.objects.all(),
                widget=fields.AutoCompleteWidget(model=Author, url='/autocomplete/')
            )

    Add data URL:

        url(r'^autocomplete/$',
            view='basic.tools.views.generic.auto_complete',
            kwargs={
                'queryset': Author.objects.all()
                'fields': ('first_name__icontains', 'last_name__icontains')
            }
        )

    """
    text_field = '%s_auto_complete'
    hidden_field = '%s'

    def __init__(self, model, url, attrs=None, required=True):
        self.attrs = attrs or {}
        self.required = required
        self.Model = model

    def render(self, name, value, attrs=None):
        text_html = self.create_input(TextInput, name, self.text_field)
        hidden_html = self.create_input(HiddenInput, name, self.hidden_field, value)

        results = ''
        if value:
            object_list = self.Model.objects.filter(pk__in=value)
            for obj in object_list:
                results += '<span class="ac_result"><a href="#%s">x</a>%s</span>\n' % (obj.pk, obj.get_full_name())

        script = '<script type="text/javascript">new AutoCompleteWidget("id_%s", "/library/autocomplete/authors/");</script>' % (self.text_field % name)
        return mark_safe(u'\n'.join([text_html, results, hidden_html, script]))

    def create_input(self, Input, name, field, value=''):
        id_ = 'id_%s' % name
        local_attrs = self.build_attrs(id=field % id_)
        i = Input()
        if type(value) == list:
            value = ','.join(['%s' % v for v in value])
        input_html = i.render(field % name, value, local_attrs)
        return input_html

    def value_from_datadict(self, data, files, name):
        hidden_data = data.get(self.hidden_field % name)
        if hidden_data:
            return hidden_data.split(',')
        return data.get(name, None)
