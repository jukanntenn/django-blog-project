from comments.models import BlogComment
from core.abstracts import AbstractEntry
from core.utils import generate_rich_content
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from model_utils import Choices
from model_utils.fields import MonitorField
from model_utils.models import TimeStampedModel

from .managers import IndexMaterialManager, MaterialManager


class Category(TimeStampedModel):
    logo = models.ImageField(_('logo'), upload_to='courses/categories/logos/', blank=True)
    logo_thumbnail = ImageSpecField(source='logo', processors=[ResizeToFill(36, 36)], format='PNG',
                                    options={'quality': 100})
    name = models.CharField(_('name'), max_length=20)
    rank = models.IntegerField(_('rank'), default=0)

    class Meta:
        ordering = ['rank', '-created']
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def __str__(self):
        return self.name


class Course(TimeStampedModel):
    STATUS = Choices(
        (0, 'writing', 'writing'),
        (1, 'finished', 'finished'),
    )
    LEVEL = Choices(
        (0, 'introductory', '入门'),
        (1, 'intermediate', '进阶'),
        (2, 'advanced', '高级'),
    )

    title = models.CharField(_('title'), max_length=150)
    slug = models.SlugField(_('slug'), unique=True)
    description = models.TextField(_('description'), blank=True)
    brief = models.CharField(_('brief'), max_length=200, blank=True)
    cover = models.ImageField(_('cover'), upload_to='courses/covers/')
    cover_thumbnail = ImageSpecField(source='cover', format='JPEG', processors=[ResizeToFill(540, 300)],
                                     options={'quality': 90})
    cover_caption = models.CharField(_('cover_caption'), max_length=100, blank=True)
    status = models.IntegerField(_('status'), choices=STATUS, default=STATUS.writing)
    status_changed = MonitorField(_('status_changed'), monitor='status')
    level = models.IntegerField(_('level'), choices=LEVEL, default=LEVEL.introductory)
    level_changed = MonitorField(_('level_changed'), monitor='level')
    rank = models.IntegerField(_('rank'), default=0)

    creator = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('creator'), on_delete=models.CASCADE)
    category = models.ForeignKey(Category, verbose_name=_('category'), on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        ordering = ('rank', '-created')
        verbose_name = _('course')
        verbose_name_plural = _('courses')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('courses:course_detail', kwargs={'slug': self.slug})

    @cached_property
    def first_material(self):
        return self.material_set.first()

    @property
    def total_views(self):
        return self.material_set.aggregate(total_views=models.Sum('views')).get('total_views') or 0

    @cached_property
    def rich_content(self):
        return generate_rich_content(self.description)


class Material(AbstractEntry):
    STATUS = Choices(
        (0, 'writing', 'writing'),
        (1, 'draft', 'draft'),
        (2, 'published', 'published'),
        (3, 'hidden', 'hidden'),
    )

    status = models.IntegerField(_('status'), choices=STATUS, default=STATUS.draft)
    status_changed = MonitorField(_('status_changed'), monitor='status')
    cover = models.ImageField(_('cover'), upload_to='covers/materials/', blank=True)
    cover_thumbnail = ImageSpecField(source='cover', format='JPEG', processors=[ResizeToFill(60, 60)],
                                     options={'quality': 90})
    cover_caption = models.CharField(_('cover_caption'), max_length=100, blank=True)
    rank = models.IntegerField(_('rank'), default=0)
    course = models.ForeignKey(Course, verbose_name=_('course'), on_delete=models.CASCADE)

    objects = MaterialManager()
    index = IndexMaterialManager()

    class Meta:
        ordering = ['rank', 'created']
        verbose_name = _('material')
        verbose_name_plural = _('materials')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('courses:material_detail', kwargs={'pk': self.pk, 'slug': self.course.slug})

    @property
    def type(self):
        return 'm'

    @cached_property
    def prev(self):
        return self.get_next_or_previous(is_next=False, value_fields=['id', 'title', 'course__slug'],
                                         course_id=self.course_id)

    @cached_property
    def next(self):
        return self.get_next_or_previous(is_next=True, value_fields=['id', 'title', 'course__slug'],
                                         course_id=self.course_id)
