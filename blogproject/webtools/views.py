from braces.views import SetHeadlineMixin
from django.views.generic import FormView

from .forms import DjangoSecretKeyCreateForm


class DjangoSecretKeyCreateView(SetHeadlineMixin, FormView):
    headline = "Django Secret Key 在线生成器"
    form_class = DjangoSecretKeyCreateForm
    template_name = "webtools/django_secret_key.html"

    def form_valid(self, form):
        return self.render_to_response(
            context={"form": form, "django_secret_key": form.create_secret_key()}
        )
