from django import template

register = template.Library()


@register.filter()
def filter_media(val):
    if val:
        return f'/media/{val}'

    return '#'


@register.simple_tag()
def tag_media(val):
    if val:
        return f'/media/{val}'

    return '#'