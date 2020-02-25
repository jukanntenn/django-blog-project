import threading

from django.contrib.sites.shortcuts import get_current_site
from django.template import loader
from django_comments.moderation import CommentModerator, Moderator
from notifications.signals import notify


class BlogModerator(Moderator):
    def post_save_moderation(self, sender, comment, request, **kwargs):
        model = comment.content_type.model_class()
        if model not in self._registry:
            return
        self._registry[model].reply(comment, comment.content_object, request)


class BlogCommentModerator(CommentModerator):
    def reply(self, comment, content_object, request):
        post_author = content_object.author

        if comment.parent:
            parent_user = comment.parent.user
            # 通知被评论的人，自己回复自己无需通知
            if parent_user != comment.user:
                reply_data = {
                    "recipient": parent_user,
                    "verb": "reply",
                    "target": comment,
                }
                notify.send(sender=comment.user, **reply_data)

                if parent_user.email and parent_user.email_bound:
                    t = loader.get_template("comments/email_reply_notification.txt")
                    c = {
                        "commenter_name": comment.user.name,
                        "comment_comment": comment.comment,
                        "post_title": content_object.title,
                        "post_url": content_object.get_absolute_url,
                        "site": get_current_site(request).domain,
                        "comment_pk": comment.pk,
                        "protocol": "http",
                    }
                    message = t.render(c)
                    email_data = {
                        "subject": "[追梦人物的博客]评论有了新回复",
                        "message": message,
                        "fail_silently": True,
                        "html_message": message,
                    }
                    threading.Thread(
                        target=parent_user.email_user, kwargs=email_data
                    ).start()

            if parent_user != content_object.author and post_author != comment.user:
                # 如果被回复的人不是文章作者，且不是文章作者自己的回复，文章作者应该收到通知
                comment_data = {
                    "recipient": post_author,
                    "verb": "comment",
                    "target": comment,
                }
                notify.send(sender=comment.user, **comment_data)
        else:
            # 如果是直接评论，且不是文章作者自己评论，则通知文章作者
            if post_author != comment.user:
                comment_data = {
                    "recipient": post_author,
                    "verb": "comment",
                    "target": comment,
                }
                notify.send(sender=comment.user, **comment_data)


moderator = BlogModerator()
