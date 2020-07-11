from django import forms
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _


class DjangoSecretKeyCreateForm(forms.Form):
    CHARS = "abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)"

    prefix = forms.CharField(max_length=10, required=False, label=_("prefix"))
    suffix = forms.CharField(max_length=10, required=False, label=_("suffix"))

    def create_secret_key(self):
        prefix = self.cleaned_data.get("prefix", "")
        suffix = self.cleaned_data.get("suffix", "")

        body_len = 50 - len(prefix) - len(suffix)
        body = get_random_string(body_len, self.CHARS)
        return "".join([prefix, body, suffix])
