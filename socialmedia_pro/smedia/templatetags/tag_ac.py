from django import template

register = template.Library()


@register.filter(name='field_type')
def field_type(field):
    fl_type = field.field.widget.__class__.__name__
    fl_type = fl_type.replace("Input", "").lower()
    return fl_type


