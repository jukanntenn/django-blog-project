from comments.models import BlogComment
from core.utils import generate_rich_content
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models import F, Q
from django.utils.functional import cached_property
from django.utils.html import strip_tags
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel


class AbstractEntry(TimeStampedModel):
    title = models.CharField(_('title'), max_length=255)
    body = models.TextField(_('body'))
    brief = models.TextField(_('brief'), blank=True)
    excerpt = models.TextField(_('excerpt'), blank=True)
    views = models.PositiveIntegerField(_('views'), default=0, editable=False)
    pub_date = models.DateTimeField(_('publication datetime'), blank=True, null=True)
    show_on_index = models.BooleanField(_('show on index'), default=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('author'), on_delete=models.CASCADE)
    comment_enabled = models.BooleanField(_('comment enabled'), default=True)
    comments = GenericRelation(BlogComment, object_id_field='object_pk', content_type_field='content_type')

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

    @property
    def toc(self):
        return self.rich_content.get('toc', '')

    @property
    def body_html(self):
        return self.rich_content.get('content', '')

    @cached_property
    def rich_content(self):
        return generate_rich_content(self.body)

    @cached_property
    def num_words(self):
        # Todo: 使用更加精确的字数统计算法
        return len(strip_tags(self.body_html))

    @cached_property
    def num_comment_participants(self):
        return self.comments.values_list('user_id', flat=True).distinct().count()

    def increase_views(self):
        self.__class__.objects.filter(pk=self.pk).update(views=F('views') + 1)

    def root_comments(self):
        return self.comments.roots()

    @cached_property
    def num_comments(self):
        return self.comments.visible().count()

    def get_next_or_previous(self, is_next, ordering=None, value_fields=None, **kwargs):
        if not self.pk:
            raise ValueError(_("get_next/get_previous cannot be used on unsaved objects."))
        op = 'gt' if is_next else 'lt'
        order = '' if is_next else '-'

        if ordering is None:
            ordering = self._meta.ordering

        if not ordering:
            ordering = ['pk']

        param_field = ordering[0]
        param_value = getattr(self, param_field)

        q = Q(**{'%s__%s' % (param_field, op): param_value})
        if not self._meta.get_field(param_field).unique:
            q = q | Q(**{param_field: param_value, 'pk__%s' % op: self.pk})

        qs = self.__class__._default_manager.filter(**kwargs).filter(q).order_by(
            *['%s%s' % (order, field) for field in ordering])

        if value_fields is not None:
            qs = qs.values(*value_fields)

        return qs.first()
