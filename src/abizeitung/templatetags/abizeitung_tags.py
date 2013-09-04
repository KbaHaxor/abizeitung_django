from django import template

register = template.Library()

@register.filter
def startswith(a, b):
    return a.startswith(b)