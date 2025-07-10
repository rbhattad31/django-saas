# core/middleware.py
from django_multitenant.utils import set_current_tenant
 

class AccountMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and not request.user.is_superuser:
            set_current_tenant(request.user.account)
        return self.get_response(request)
 