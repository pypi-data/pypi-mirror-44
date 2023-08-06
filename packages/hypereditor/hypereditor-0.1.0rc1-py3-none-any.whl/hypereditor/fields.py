import json
import random
import string

from django import forms, template
from django.db import models
from django.utils.safestring import mark_safe

from .blocks import get_block_class_for
from .blocks.base import CodeRenderer
from django.template.loader import render_to_string


class HyperWidget(forms.widgets.Textarea):
    template_name = 'hypereditor/widgets/hyper_widget.html'

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['identifier'] = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        return context


class HyperFormField(forms.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['widget'] = HyperWidget(attrs={'id': 'hyperHiddenField'})
        super(HyperFormField, self).__init__(*args, **kwargs)


class HyperFieldResponse(object):

    def __init__(self, value_dict):
        self.data = value_dict

    def from_str(str_data):
        data = json.loads(str_data)
        return HyperFieldResponse(data)

    def render(self, context=None):
        rendered_data = ''
        if isinstance(context, template.Context) or isinstance(context, template.RequestContext):
            context = context.flatten()
        codeRenderer = CodeRenderer()
        for item in self.data:
            bl_class = get_block_class_for(item.get('type', 'INVALID_PLUGIN_WITH_NO_TYPE'))
            if bl_class:
                instance = bl_class(codeRenderer)
                rendered_data = rendered_data + instance.render(item, context)

        rendered_data = codeRenderer.renderCSS() + rendered_data + codeRenderer.renderJS()
        return mark_safe(rendered_data)

    def get_prep_value(self):
        return json.dumps(self.data)

    def __str__(self):
        return self.get_prep_value()


class HyperField(models.Field):

    def get_internal_type(self):
        return 'TextField'

    def formfield(self, **kwargs):
        defaults = {'form_class': HyperFormField}
        defaults.update(kwargs)
        return super().formfield(**defaults)

    def to_python(self, value):
        if isinstance(value, HyperFieldResponse):
            return value

        if value is not None and value != '':
            try:
                value_dict = json.loads(value)
                return HyperFieldResponse(value_dict)
            except Exception as e:
                print(value)
                return HyperFieldResponse(None)
        else:
            return []

    def from_db_value(self, value, expression, connection, context):
        return self.to_python(value)

    def get_prep_value(self, value):
        if isinstance(value, HyperFieldResponse):
            return value.get_prep_value()
        else:
            return value

    def value_to_string(self, obj):
        value = self.value_from_object(obj)
        return self.get_prep_value(value)
