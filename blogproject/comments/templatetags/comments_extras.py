from django import template
from django.contrib.contenttypes.models import ContentType
from rest_framework.authtoken.models import Token

register = template.Library()


@register.inclusion_tag('comments/inclusions/_comments_app.html', takes_context=True)
def show_comment_app(context, target):
    num_comments = context['num_comments']
    num_comment_participants = context['num_comment_participants']
    user = context['user']
    app_label, model = ContentType.objects.get_for_model(target).natural_key()
    content_type = '{}.{}'.format(app_label, model)
    object_pk = target.pk
    token = ''
    if user.is_authenticated:
        try:
            token = user.auth_token.key
        except Token.DoesNotExist:
            pass
    return {
        'content_type': content_type,
        'object_pk': object_pk,
        'token': token,
        'num_comments': num_comments,
        'num_comment_participants': num_comment_participants,
    }
