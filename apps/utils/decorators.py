from django.http import HttpResponseBadRequest


def is_ajax(function):
    def wrap(request, *args, **kwargs):
        if request.is_ajax():
            return function(request, *args, **kwargs)
        else:
            raise HttpResponseBadRequest
        wrap.__doc__ = function.__doc__
        wrap.__name__ = function.__name__
        return wrap
