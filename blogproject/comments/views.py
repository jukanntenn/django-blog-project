import time
from collections import deque

from django.apps import apps
from django.contrib import messages as dj_messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.utils.decorators import method_decorator
from django.utils.html import escape
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, RedirectView, View
from django.views.generic.edit import FormMixin
from rest_framework import mixins, serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

import django_comments as comments
from braces.views import AjaxResponseMixin, CsrfExemptMixin, JSONResponseMixin, SetHeadlineMixin
from django_comments import get_form, signals
from users.models import User

from .forms import BlogCommentForm
from .models import BlogComment
from .serializers import CommentSerializer, TreeCommentSerializer
from .utils import generate_security_hash


class CommentViewSet(
    mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet
):
    serializer_class = TreeCommentSerializer
    pagination_class = LimitOffsetPagination

    # csrf 已由 security hash 保护
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        return response

    def initial(self, request, *args, **kwargs):
        self._check_params()
        super().initial(request, *args, **kwargs)

    def get_permissions(self):
        permissions = super().get_permissions()
        if self.action == "create":
            permissions.append(IsAuthenticated())
        return permissions

    def get_serializer_class(self):
        if self.action == "list":
            return TreeCommentSerializer
        return CommentSerializer

    def _check_params(self):
        """检查被评论对象 ContentType 参数的合法性"""

        request = self.request
        ctype = request.GET.get("content_type") or request.data.get("content_type")
        object_pk = request.GET.get("object_pk") or request.data.get("object_pk")

        if ctype is None or object_pk is None:
            raise ValidationError(
                {"detail": "Missing content_type or object_pk field."}
            )
        try:
            model = apps.get_model(*ctype.split(".", 1))
            target = model._default_manager.get(pk=object_pk)
            target_ct = ContentType.objects.get_for_model(target)
            self.target = target
            self.target_ct = target_ct
        except TypeError:
            raise ValidationError(
                {"detail": "Invalid content_type value: %r" % escape(ctype)}
            )
        except AttributeError:
            raise ValidationError(
                {
                    "detail": "The given content-type %r does not resolve to a valid model."
                },
            )
        except ObjectDoesNotExist:
            raise ValidationError(
                {
                    "detail": "No object matching content-type %r and object PK %r exists."
                    % (escape(ctype), escape(object_pk))
                }
            )
        except (ValueError, serializers.ValidationError) as e:
            raise ValidationError(
                {
                    "detail": "Attempting go get content-type %r and object PK %r exists raised %s"
                    % (escape(ctype), escape(object_pk), e.__class__.__name__)
                }
            )

    def _check_form(self):
        """数据合法性检查"""
        target = self.target
        data = self.request.data.copy()
        data["user"] = self.request.user
        # data['name'] = self.request.user.username
        self.form = get_form()(target, data=data)

        if self.form.security_errors():
            raise ValidationError(
                {
                    "detail": "The comment form failed security verification: %s"
                    % escape(str(self.form.security_errors()))
                }
            )
        if self.form.errors:
            raise ValidationError({"detail": self.form.errors})

    def get_queryset(self):
        target = self.target
        target_ct = self.target_ct
        root_comments = BlogComment.objects.root_nodes().filter(
            content_type=target_ct, object_pk=target.pk
        )
        qs = root_comments.get_descendants(include_self=True).select_related(
            "user", "parent__user"
        )
        # Todo: 使用子查询优化头像的获取
        qs = qs.prefetch_related(
            "user__socialaccount_set", "parent__user__socialaccount_set"
        )

        # 将 [root1, descendant1, descendant2, root2, descendant3, descendant4, root3]
        # 转换为：[root1, root2, root3]，root.descendants = [descendantx, descendanty]

        root_comments_rv = reversed(root_comments)
        root = next(root_comments_rv, None)
        descendants = deque()
        for comment in reversed(qs):
            if comment.pk == root.pk:
                root.descendants = list(descendants)
                root = next(root_comments_rv, None)
                if root is None:
                    break
                descendants = deque()
                continue
            descendants.appendleft(comment)
        return root_comments

    def create(self, request, *args, **kwargs):
        self._check_form()
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        request = self.request
        site = get_current_site(request)
        # Todo: use ipaware
        ip_address = request.META.get("REMOTE_ADDR", None) or None
        user = request.user

        comment = self.form.get_comment_object(site_id=site.id)
        comment.ip_address = ip_address
        comment.user = user
        responses = signals.comment_will_be_posted.send(
            sender=comment.__class__, comment=comment, request=request
        )
        for (receiver, response) in responses:
            if response is False:
                return Response(
                    data={
                        "detail": "comment_will_be_posted receiver %r killed the comment"
                        % receiver.__name__
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

        serializer.save(comment=comment)
        signals.comment_was_posted.send(
            sender=comment.__class__, comment=comment, request=request
        )

    @action(methods=["get"], detail=False, url_path="security-data")
    def security_data(self, request):
        content_type = request.query_params.get("content_type")
        object_pk = request.query_params.get("object_pk")

        if not (content_type and object_pk):
            return Response({"detail": "请求参数错误！"}, status=status.HTTP_400_BAD_REQUEST)

        timestamp = str(int(time.time()))
        security_hash = generate_security_hash(content_type, object_pk, timestamp)
        security_dict = {
            "content_type": content_type,
            "object_pk": object_pk,
            "timestamp": str(timestamp),
            "security_hash": security_hash,
        }
        return Response(data=security_dict, status=status.HTTP_200_OK)


class CommentReplyView(LoginRequiredMixin, FormMixin, SetHeadlineMixin, DetailView):
    headline = "回复评论"
    model = BlogComment
    form_class = BlogCommentForm
    pk_url_kwarg = "pid"
    template_name = "comments/reply.html"

    def get_form_kwargs(self):
        kwargs = super(CommentReplyView, self).get_form_kwargs()
        kwargs.update(
            {"target_object": self.object.content_object, "parent": self.object.pk}
        )
        return kwargs


class CommentSuccess(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        self.url = self.comment.get_absolute_url()
        return super(CommentSuccess, self).get_redirect_url(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.comment = None
        if "c" in request.GET:
            try:
                self.comment = comments.get_model().objects.get(pk=request.GET["c"])
            except (ObjectDoesNotExist, ValueError):
                pass
        if self.comment and self.comment.is_public:
            return super(CommentSuccess, self).get(request, *args, **kwargs)


class SendVerificationCodeView(
    CsrfExemptMixin, LoginRequiredMixin, JSONResponseMixin, AjaxResponseMixin, View
):
    raise_exception = True

    def post_ajax(self, request, *args, **kwargs):
        messages = {
            "msg": "",
            "ok": 0,
        }

        email = request.POST.get("email")

        if not email:
            messages["msg"] = "请输入邮箱地址"
            return self.render_json_response(messages)

        try:
            validate_email(email)
        except ValidationError:
            messages["msg"] = "请输入合法的邮箱地址"
            return self.render_json_response(messages)

        try:
            user = User.objects.get(email=email)
            if user != request.user:
                messages["msg"] = "该邮箱已被其他用户绑定"
                return self.render_json_response(messages)
        except User.DoesNotExist:
            pass

        # email 合法，处理验证码
        expire_at = request.session.get("expire_at")

        if not expire_at or expire_at < timezone.now().timestamp():
            # 没有设置验证码或者验证码过期
            verification_code = get_random_string(length=6, allowed_chars="0123456789")
            request.session["verification_code"] = verification_code
            expire_at = timezone.now() + timezone.timedelta(minutes=5)
            request.session["expire_at"] = expire_at.timestamp()
        else:
            verification_code = request.session["verification_code"]
            verification_email = request.session["email"]

            if email != verification_email:
                verification_code = get_random_string(
                    length=6, allowed_chars="0123456789"
                )
                request.session["verification_code"] = verification_code
                expire_at = timezone.now() + timezone.timedelta(minutes=5)
                request.session["expire_at"] = expire_at.timestamp()

        # 发送邮件
        send_mail(
            subject="[追梦人物的博客]请验证你的邮箱",
            message="你正在验证评论回复接收邮箱，验证码为 %s ,有效时间5分钟。" % verification_code,
            from_email=None,
            recipient_list=[email],
            fail_silently=True,
        )

        request.session["email"] = email
        messages["ok"] = 1
        messages["msg"] = "验证码已发送到你的邮箱"
        return self.render_json_response(messages)


class EmailBindingView(
    CsrfExemptMixin, LoginRequiredMixin, JSONResponseMixin, AjaxResponseMixin, View
):
    raise_exception = True

    def post_ajax(self, request, *args, **kwargs):

        messages = {
            "msg": "",
            "ok": 0,
        }
        email = request.POST.get("email")
        code = request.POST.get("verification_code")

        if not email:
            messages["msg"] = "请输入邮箱地址"
            return self.render_json_response(messages)

        if not code:
            messages["msg"] = "请输入验证码"
            return self.render_json_response(messages)

        verification_email = request.session.get("email")
        verification_code = request.session.get("verification_code")

        if not verification_code or not verification_email:
            messages["msg"] = "请先获取验证码"
            return self.render_json_response(messages)

        if email != verification_email:
            messages["msg"] = "提交的邮箱与接收验证码的邮箱不一致"
            return self.render_json_response(messages)

        if code != verification_code:
            messages["msg"] = "验证码错误"
            return self.render_json_response(messages)

        expire_at = request.session.get("expire_at")

        if expire_at < timezone.now().timestamp():
            messages["msg"] = "验证码已过期，请重新获取"
            return self.render_json_response(messages)

        request.user.email = email
        request.user.email_bound = True
        request.user.save(update_fields=["email", "email_bound"])

        del request.session["email"]
        del request.session["verification_code"]
        del request.session["expire_at"]

        messages["ok"] = 1
        dj_messages.success(request, "邮箱绑定成功")
        return self.render_json_response(messages)
