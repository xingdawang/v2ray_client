from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponseNotFound

class Custom404Middleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if response.status_code == 404 and settings.DEBUG:
            return render(request, 'users/components/404.html', status=404)

        return response