from django.http import HttpResponseRedirect
from django.urls import reverse

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.public_urls = ['login', 'register']

    def __call__(self, request):
        if not request.user.is_authenticated:
            current_url = request.resolver_match.url_name if request.resolver_match else None
            if current_url not in self.public_urls:
                return HttpResponseRedirect(reverse('login') + '?next=' + request.path)
        response = self.get_response(request)
        return response