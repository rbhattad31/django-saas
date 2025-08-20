

# from django.http import HttpResponseRedirect
# from django.urls import reverse
# from rest_framework.views import exception_handler
# from django.shortcuts import render
# from django.core.exceptions import PermissionDenied

# def custom_exception_handler(exc, context):
#     response = exception_handler(exc, context)
    

#     # If it's PermissionDenied -> show your template
#     if isinstance(exc, PermissionDenied):
#         request = context.get("request")
#         return HttpResponseRedirect(reverse('forbidden_page'))

#     return None

