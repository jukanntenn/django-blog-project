from django import forms
from django.utils.translation import gettext_lazy as _
from django_comments.forms import COMMENT_MAX_LENGTH, CommentForm

from . import get_model


class BlogCommentForm(CommentForm):
    parent = forms.IntegerField(required=False, widget=forms.HiddenInput)
    comment = forms.CharField(label=_("Comment"), max_length=COMMENT_MAX_LENGTH)

    def __init__(self, target_object, parent=None, data=None, initial=None, **kwargs):
        self.parent = parent
        if initial is None:
            initial = {}
        initial.update({"parent": self.parent.pk})
        super().__init__(target_object, data=data, initial=initial, **kwargs)
        self.fields["email"].required = False
        self.fields["name"].required = False

    def get_comment_model(self):
        return get_model()

    def get_comment_create_data(self, **kwargs):
        d = super().get_comment_create_data()
        d["parent_id"] = self.cleaned_data["parent"]
        return d
