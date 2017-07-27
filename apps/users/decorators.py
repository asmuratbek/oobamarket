from django.utils.six import wraps
from django.http import HttpResponseForbidden


def user_profile_permission(function):
    @wraps(function)
    def decorator(request, *args, **kwargs):
        user = request.user
        username = kwargs['username']
        if user.username != username:
            return HttpResponseForbidden()
        return function
    return decorator
