import threading

from constance import config
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template import loader
from django_comments.moderation import CommentModerator, Moderator
from notifications.signals import notify


class BlogModerator(Moderator):
    def post_save_moderation(self, sender, comment, request, **kwargs):
        model = comment.content_type.model_class()
        if model not in self._registry:
            return
        self._registry[model].notify(comment, comment.content_object, request)


class BlogCommentModerator(CommentModerator):
    email_notification = True
    enable_field = "comment_enabled"

    def notify(self, comment, content_object, request):
        author = content_object.author
        notification_data = []
        if comment.user != author:
            # 博主接收的通知
            notification_data.append(
                {"recipient": author, "verb": "comment", "target": comment}
            )

        if comment.parent:
            parent_user = comment.parent.user
            # 不是自己评论自己，通知被评论者
            if comment.user != parent_user:
                notification_data.append(
                    {"recipient": parent_user, "verb": "reply", "target": comment}
                )

        if not notification_data:
            return

        for data in notification_data:
            notify.send(sender=comment.user, **data)
            recipient = data["recipient"]
            if recipient == author or not recipient.email_bound:
                continue

            t = loader.get_template("comments/reply_notification_email.html")
            c = {
                "comment": comment,
                "content_object": content_object,
                "site": get_current_site(request),
                "link": request.build_absolute_uri(content_object.get_absolute_url())
                + "#c"
                + str(comment.pk),
            }
            message = t.render(c)
            email_data = {
                "subject": config.REPLY_EMAIL_SUBJECT,
                "message": message,
                "from_email": settings.DEFAULT_FROM_EMAIL,
                "fail_silently": True,
                "html_message": message,
            }
            recipient.email_user(**email_data)

        if comment.user != author:
            self.email(comment, content_object, request)


moderator = BlogModerator()
