from django_multitenant.utils import set_current_tenant
from core.models import Account

class AccountMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            try:
                account = request.user.account
                set_current_tenant(account)
            except AttributeError:
                set_current_tenant(None)
        else:
            set_current_tenant(None)
        response = self.get_response(request)
        return response