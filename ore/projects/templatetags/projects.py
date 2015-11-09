from django import template

register = template.Library()

@register.filter
def contains_user(queryset, user):
    return queryset.filter(pk=user.pk).exists()
