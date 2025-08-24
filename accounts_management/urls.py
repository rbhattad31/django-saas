# from django.shortcuts import render
# # accounts_management/urls.py
# from django.urls import path
# from .views import UserListView, UserDataListView

# app_name = 'accounts_management'

# urlpatterns = [
#     path('api/user-list/', UserListView.as_view(), name='api-user-list'),
#     path('api/user-data-list/', UserDataListView.as_view(), name='api-user-data-list'),
#     path('api/user-create/', lambda request: render(request, 'home/user_create.html'), name='api-user-create'),
#     path('api/user-edit/<int:pk>/', lambda request, pk: render(request, 'home/user_edit.html', {'pk': pk}), name='api-user-edit'),
#     path('api/user-view/<int:pk>/', lambda request, pk: render(request, 'home/user_view.html', {'pk': pk}), name='api-user-view'),
# ]

from django.urls import path
from django.shortcuts import render
from .views import UserListView, UserDataListView, UserCreateView, UserDetailView, UserViewView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('api/user-list/', UserListView.as_view(), name='api-user-list'),
    path('api/user-data-list/', UserDataListView.as_view(), name='api-user-data-list'),
    path('api/user-create/', UserCreateView.as_view(), name='api-user-create'),
    path('api/user-detail/<int:pk>/', UserDetailView.as_view(), name='api-user-detail'),
    path('api/user-view/<int:pk>/', UserViewView.as_view(), name='api-user-view'),
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
