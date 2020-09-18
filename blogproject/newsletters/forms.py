from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Subscription


class SubscriptionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super(SubscriptionForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Subscription
        fields = ["email"]

    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            subscription = Subscription.objects.get(email=email)
            if subscription.confirmed:
                raise forms.ValidationError(_("Already subscribed!"))
            else:
                subscription.delete()
        except Subscription.DoesNotExist:
            pass

        return email

    def save(self, commit=True):
        subscription = super().save(commit=False)
        if self.user and self.user.is_authenticated:
            subscription.user = self.user

        if commit:
            subscription.save()
        return subscription
