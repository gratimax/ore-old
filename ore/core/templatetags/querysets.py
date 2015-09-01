from django import template

register = template.Library()

@register.filter
def all(queryset):
    return queryset.all()
