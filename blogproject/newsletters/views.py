from constance import config
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.template import loader
from django.urls import reverse
from django.views.generic import CreateView, View

from braces.views import FormValidMessageMixin, MessageMixin, SetHeadlineMixin
from core.utils import EmailConfirmation
from favorites.models import Issue
from ratelimit.decorators import ratelimit

from .forms import SubscriptionForm


# Todo
# 1. 邮件改异步发送
# 2. 订阅接口限流
# 3. 邮件推送订阅内容
# 4. 引入 sortableadmin2，celery，mailhog
class SubscriptionCreateView(SetHeadlineMixin, FormValidMessageMixin, CreateView):
    form_class = SubscriptionForm
    template_name = "newsletters/subscription.html"
    form_valid_message = "感谢订阅每周精选收藏，确认邮件已发至您的订阅邮箱，请及时前往确认。如长时间没有收到确认邮件，请尝试重新订阅或联系博主。"
    headline = "订阅每周精选收藏"

    @ratelimit(key="ip", rate="3/h", method="POST")
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        confirmation = EmailConfirmation(instance=self.object)
        subject = config.NEWSLETTERS_SUBSCRIPTION_CONFIRMATION_SUBJECT
        html_message = loader.render_to_string(
            "newsletters/subscription_confirmation_email.html",
            context={
                "link": self.request.build_absolute_uri(
                    reverse(
                        "newsletters:subscription-confirm",
                        kwargs={"key": confirmation.make_key()},
                    )
                ),
            },
        )
        # Todo: 异步任务发送
        send_mail(
            subject=subject,
            message=html_message,
            html_message=html_message,
            from_email=None,
            recipient_list=[self.object.email],
        )
        return response

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse("newsletters:subscription")

    def get_context_data(self, **kwargs):
        issue = Issue.objects.all().order_by("-number").first()
        favorite_list = (
            issue.favorites.all().order_by("rank", "-created_at") if issue else []
        )
        context = super().get_context_data(**kwargs)
        context.update({"issue": issue, "favorite_list": favorite_list})
        return context


class SubscriptionConfirmView(MessageMixin, View):
    def get(self, request, *args, **kwargs):
        confirmation = EmailConfirmation.from_key(self.kwargs["key"])
        if confirmation is None:
            self.messages.error("订阅链接已失效，请重新订阅。", extra_tags="danger")
            return redirect("newsletters:subscription")

        if confirmation.instance.confirmed:
            self.messages.warning("订阅邮箱已确认，无需重复确认。")
        else:
            confirmation.instance.confirm()
            self.messages.success("订阅成功！")
        return redirect("favorites:issue_list")
