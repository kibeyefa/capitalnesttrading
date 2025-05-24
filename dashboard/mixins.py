from django.contrib.auth.mixins import LoginRequiredMixin
from allauth.account.models import EmailAddress
from django.http import HttpResponseForbidden
from django.shortcuts import redirect


class EmailVerifiedRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        try:
            if not EmailAddress.objects.filter(
                user=request.user, verified=True
            ).exists():
                return redirect("account_email_verification_sent")
            return super().dispatch(request, *args, **kwargs)
        except:
            return super().dispatch(request, *args, **kwargs)
