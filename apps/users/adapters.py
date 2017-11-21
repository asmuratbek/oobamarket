from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class AccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request):
        return getattr(settings, 'ACCOUNT_ALLOW_REGISTRATION', True)

    def get_login_redirect_url(self, request):
        path = "/"
        return path


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_open_for_signup(self, request, sociallogin):
        return getattr(settings, 'ACCOUNT_ALLOW_REGISTRATION', True)

    def get_login_redirect_url(self, request):
        path = "/"
        return path

    def is_auto_signup_allowed(self, request, sociallogin):
        if request.GET.get('is_mobile', '0') == '1':
            return True

        return super().is_auto_signup_allowed(request, sociallogin)


