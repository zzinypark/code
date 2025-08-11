from django import template

register = template.Library()


@register.simple_tag()
def add_like_class(user, likes):
    for like_object in likes:
        if like_object.user == user:
            return "text-danger"
    return ""
