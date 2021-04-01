from braces.views import CsrfExemptMixin, JSONResponseMixin
from django.core import mail
from django.views.generic import View


class SingleEmailDebugView(CsrfExemptMixin, JSONResponseMixin, View):
    """A view that sending a single email for debug purpose"""

    def post(self, request, *args, **kwargs):
        mail.send_mail(
            subject="Hello World",
            message="Let's say hello to the world.",
            from_email="helloworld@example.com",
            recipient_list=["test@example.com"],
        )
        return self.render_json_response({"code": 1, "msg": "ok"})


class MassEmailDebugView(CsrfExemptMixin, JSONResponseMixin, View):
    """A view that sending mass emails for debug purpose"""

    def post(self, request, *args, **kwargs):
        emails = (
            (
                "Hey Man",
                "I'm The Dude! So that's what you call me.",
                "dude@aol.com",
                ["mr@lebowski.com"],
            ),
            (
                "Dammit Walter",
                "Let's go bowlin'.",
                "dude@aol.com",
                ["wsobchak@vfw.org"],
            ),
        )
        mail.send_mass_mail(emails)
        return self.render_json_response({"code": 1, "msg": "ok"})
