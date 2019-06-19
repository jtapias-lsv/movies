from django import template

register = template.Library()

@register.filter
def own_format_float(value):
    return "{0:.2f}".format(value)