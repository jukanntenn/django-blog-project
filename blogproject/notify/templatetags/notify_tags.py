from django import template
from django.conf import settings
from django.template.loader import render_to_string

register = template.Library()


@register.simple_tag
def display(obj, request=None):
    tpl = getattr(settings, 'NOTIFICATION_TEMPLATES').get(obj.verb)

    if not tpl:
        return ''

    context = {
        'notification': obj,
        'actor': obj.actor,
        'target': obj.target,
        'request': request,
    }
    return render_to_string(tpl, context=context)


@register.filter
def frag(notification):
    verb = notification.verb
    return 'notifications/inclusions/_{verb}.html'.format(verb=verb)
