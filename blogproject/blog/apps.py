from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class BlogConfig(AppConfig):
    name = 'blog'
    verbose_name = _('blog')

    def ready(self):
        from comments.moderation import moderator
        from comments.moderation import BlogCommentModerator
        from courses.models import Material
        moderator.register(self.get_model('Post'), BlogCommentModerator)
        moderator.register(Material, BlogCommentModerator)
