from django import template

register = template.Library()

@register.filter
def own_format_float(value):
    """
    function that make a custom format to a value
    Args:
        value: (float) number to be formated

    Returns: number whit format

    """
    return "{0:.2f}".format(value)