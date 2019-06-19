from django.core.cache import cache
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy

from movies_app.models import ValidatorToken


class SimpleMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        count = cache.get(request.META.get('PATH_INFO')) or 0
        count += 1
        cache.set(request.META.get('PATH_INFO'), count)
        response = self.get_response(request)
        return response


class VerificationMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response


    def __call__(self, request):

        try:
            postman_token = request.META.get('HTTP_AUTHORIZATION','')

            if ValidatorToken.objects.filter(unique_id=postman_token).exists():
                data = ValidatorToken.objects.get(unique_id=postman_token)
                request.user = data.user
            # elif ValidatorToken.objects.count()>0:
            #     data = ValidatorToken.objects.first()
            #     request.user = data.user
            # elif request.META.get('PATH_INFO') != '/login/':
            #     #if request.user.is_anonymous:
            #     return redirect('mylogin')
        except Exception:
            pass

        response = self.get_response(request)
        return response

