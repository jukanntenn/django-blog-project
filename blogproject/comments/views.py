import functools
from collections import deque

from allauth.socialaccount.models import SocialAccount
from core.decrators import field_whitelist
from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Prefetch
from django.utils.decorators import method_decorator
from django.utils.html import escape
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django_comments import get_form, signals
from drf_spectacular.utils import extend_schema, inline_serializer
from ipware import get_client_ip
from rest_framework import mixins, serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from .models import BlogComment
from .serializers import CommentSerializer, TreeCommentSerializer


class IsModerator(IsAdminUser):
    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class IsCreator(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.user


IsModeratorOrCreator = IsModerator | IsCreator


def inject_comment_target(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        viewset = args[0]
        request = viewset.request
        if request.method.upper() in {"POST"}:
            ctype = request.data.get("content_type")
            object_pk = request.data.get("object_pk")
        else:
            ctype = request.query_params.get("content_type")
            object_pk = request.query_params.get("object_pk")

        if not (ctype or object_pk):
            return Response(
                {"detail": _("Missing content_type or object_pk field.")},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            model = apps.get_model(*ctype.split(".", 1))
            target = model.objects.get(pk=object_pk)
            target_ct = ContentType.objects.get_for_model(target)
            viewset.kwargs["target"] = target
            viewset.kwargs["target_ct"] = target_ct
        except TypeError:
            return Response(
                {"detail": _("Invalid content_type value: %r" % escape(ctype))},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except AttributeError:
            return Response(
                {
                    "detail": _(
                        "The given content-type %r does not resolve to a valid model."
                        % escape(ctype)
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        except ObjectDoesNotExist:
            return Response(
                {
                    "detail": _(
                        "No object matching content-type %r and object PK %r exists."
                        % (escape(ctype), escape(object_pk))
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        except (ValueError, LookupError, ValidationError) as e:
            return Response(
                {
                    "detail": _(
                        "Attempting go get content-type %r and "
                        "object PK %r exists raised %s"
                        % (escape(ctype), escape(object_pk), e.__class__.__name__)
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        return func(*args, **kwargs)

    wrapper.__wrapped__ = func
    return wrapper


@method_decorator(
    name="destroy",
    decorator=extend_schema(
        summary="Remove comment",
    ),
)
class CommentViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = TreeCommentSerializer
    pagination_class = LimitOffsetPagination
    queryset = BlogComment.objects.visible()
    permission_classes = [AllowAny]

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    @extend_schema(
        summary="Return comments tree",
    )
    @inject_comment_target
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_permissions(self):
        if self.action == "create":
            return [IsAuthenticated()]
        if self.action == "destroy":
            return [IsAuthenticated(), IsModerator()]
        if self.action in {"update", "partial_update"}:
            return [IsAuthenticated(), IsModeratorOrCreator()]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == "list":
            return TreeCommentSerializer
        return CommentSerializer

    def filter_queryset(self, queryset):
        if self.action not in {"list"}:
            return super().filter_queryset(queryset)

        root_comments = super().filter_queryset(queryset)
        qs = (
            BlogComment.objects.get_queryset_descendants(
                queryset=root_comments.select_related("user"), include_self=True
            )
            .select_related("user", "parent", "parent__user")
            .prefetch_related(
                Prefetch(
                    "user__socialaccount_set",
                    queryset=SocialAccount.objects.all(),
                    to_attr="socialaccounts",
                ),
                Prefetch(
                    "parent__user__socialaccount_set",
                    queryset=SocialAccount.objects.all(),
                    to_attr="socialaccounts",
                ),
            )
        )
        # root_comments.select_related("user")

        # 将 [root1, descendant1, descendant2, root2, descendant3, descendant4, root3]
        # 转换为：
        # [
        #   root1 (descendants = [descendant1, descendant2]),
        #   root2 (descendants = [descendant3, descendant4]),
        #   root3 (descendants = []),
        # ]
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

    def get_queryset(self):
        if self.action not in {"list"}:
            return super().get_queryset()

        target = self.kwargs.pop("target")
        target_ct = self.kwargs.pop("target_ct")
        root_comments = (
            BlogComment.objects.roots()
            .filter(content_type=target_ct, object_pk=target.pk)
            .prefetch_related(
                Prefetch(
                    "user__socialaccount_set",
                    queryset=SocialAccount.objects.all(),
                    to_attr="socialaccounts",
                ),
            )
        )
        return root_comments

    @extend_schema(
        summary="Create a comment",
        responses={200: CommentSerializer},
    )
    @inject_comment_target
    def create(self, request, *args, **kwargs):
        target = self.kwargs.pop("target")
        data = self.request.data.copy()
        data["user"] = self.request.user
        form = get_form()(target, data=data)

        if form.security_errors():
            raise ValidationError(
                {
                    "detail": _("The comment form failed security verification: %s")
                    % escape(str(form.security_errors()))
                }
            )

        if form.errors:
            return Response(
                {"detail": form.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        site = get_current_site(request)
        ip_address, is_routable = get_client_ip(request)
        comment = form.get_comment_object(site_id=site.id)
        comment.ip_address = ip_address
        comment.user = request.user
        responses = signals.comment_will_be_posted.send(
            sender=comment.__class__, comment=comment, request=request
        )
        for (receiver, response) in responses:
            if response is False:
                return Response(
                    data={
                        "detail": _(
                            "comment_will_be_posted receiver %r killed the comment"
                        )
                        % receiver.__name__
                    },
                    status=status.HTTP_412_PRECONDITION_FAILED,
                )

        comment.save()
        signals.comment_was_posted.send(
            sender=comment.__class__, comment=comment, request=request
        )

        serializer = CommentSerializer(instance=comment, context={"request": request})
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_destroy(self, instance):
        instance.is_removed = True
        instance.save(update_fields=["is_removed"])

    @extend_schema(exclude=True)
    @field_whitelist(fields=["comment"], raise_exception=True)
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        summary="Edit comment",
        request=inline_serializer(
            "UpdateCommentSerializer", fields={"comment": serializers.CharField()}
        ),
        responses={200: CommentSerializer},
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        summary="Get security data",
        responses={200: {"pong": "timestamp in milliseconds."}},
    )
    @inject_comment_target
    @action(methods=["get"], detail=False, url_path="security-data")
    def security_data(self, request, *args, **kwargs):
        target = self.kwargs.pop("target")
        form = get_form()(target)
        return Response(data=form.generate_security_data(), status=status.HTTP_200_OK)
