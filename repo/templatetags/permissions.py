from django import template

register = template.Library()

@register.assignment_tag
def permitted(user, permslug, obj):
    return obj.user_has_permission(user, permslug)
