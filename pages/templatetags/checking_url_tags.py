from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def dynamic_link(context, section, url_name):
    request = context.get("request")
    if request and request.path == f"/{request.LANGUAGE_CODE}/":
        return f"#{section}"
    return f"{url_name}"
