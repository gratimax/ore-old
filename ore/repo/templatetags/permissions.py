from django import template
from django.template import TemplateSyntaxError
from django.utils import six

register = template.Library()

Node, NodeList = template.Node, template.NodeList

@register.filter
def as_user(value, arg):
    return value.as_user(arg)

@register.assignment_tag
def permitted(user, permslug, obj):
    return obj.user_has_permission(user, permslug)


class IfPermittedNode(Node):
    child_nodelists = ('nodelist_true', 'nodelist_false')

    def __init__(self, user, permissions, object, nodelist_true, nodelist_false, negate, check_any):
        self.user, self.permissions, self.object = user, permissions, object
        self.nodelist_true, self.nodelist_false = nodelist_true, nodelist_false
        self.negate = negate
        self.check_any = check_any

    def __repr__(self):
        return "<IfPermittedNode>"

    def render(self, context):
        user = self.user.resolve(context, True)
        permissions = self.permissions.resolve(context, True)
        if isinstance(permissions, six.string_types):
            permissions = permissions.split(',')
        object = self.object.resolve(context, True)
        check_func = any if self.check_any else all
        result = check_func((object.user_has_permission(user, permission) for permission in permissions))
        if result != self.negate:
            return self.nodelist_true.render(context)
        return self.nodelist_false.render(context)


def do_ifpermitted(parser, token, negate, check_any):
    bits = list(token.split_contents())
    if len(bits) != 4:
        raise TemplateSyntaxError("%r takes three arguments - the user, the permission and the object" % bits[0])
    end_tag = 'end' + bits[0]
    nodelist_true = parser.parse(('else', end_tag))
    token = parser.next_token()
    if token.contents == 'else':
        nodelist_false = parser.parse((end_tag,))
        parser.delete_first_token()
    else:
        nodelist_false = NodeList()
    user = parser.compile_filter(bits[1])
    permission = parser.compile_filter(bits[2])
    object = parser.compile_filter(bits[3])
    return IfPermittedNode(user, permission, object, nodelist_true, nodelist_false, negate, check_any)

@register.tag
def ifpermitted(parser, token):
    return do_ifpermitted(parser, token, False, False)

@register.tag
def ifnotpermitted(parser, token):
    return do_ifpermitted(parser, token, True, False)

@register.tag
def ifanypermitted(parser, token):
    return do_ifpermitted(parser, token, False, True)

@register.tag
def ifnotanypermitted(parser, token):
    return do_ifpermitted(parser, token, True, True)
