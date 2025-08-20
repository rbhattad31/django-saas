

# from rest_framework.views import exception_handler
# from django.shortcuts import render
# from django.core.exceptions import PermissionDenied

# def custom_exception_handler(exc, context):
#     response = exception_handler(exc, context)

#     # If DRF already handled it, return as JSON
#     if response is not None:
#         return response

#     # If it's PermissionDenied -> show your template
#     if isinstance(exc, PermissionDenied):
#         request = context.get("request")
#         return render(request, "home/page-403.html", status=403)

#     return None

