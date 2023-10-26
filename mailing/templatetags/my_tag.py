from django import template

register = template.Library()


@register.filter()
def mediapath(text):
    if text:
        return f"/media/{text}"
    else:
        return '#'
