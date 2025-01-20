from django import template
from django.conf import settings

register=template.Library()

@register.filter
def active_and_approved_comments(comments):
    return comments.filter(active=True, status=settings.COMMENT_STATUS_APPROVED)
    # return comments.exclude(active=False, status__in=['w','na'])