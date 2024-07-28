from django import template

register = template.Library()

@register.filter
def get_form_field(form, field_name):
    return form[field_name]

@register.filter
def get_radio_button(field, value):
    return field.as_widget(attrs={'value': value})