from django.conf.urls import url
from .views import (
    FacebookLogin,
    GoogleLogin
)

urlpatterns = [
    url(r'^rest-auth/facebook/$', FacebookLogin.as_view(), name='fb_login'),
    url(r'^rest-auth/google/$', GoogleLogin.as_view(), name='google_login'),
]
