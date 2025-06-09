# from django.urls import path
# from .views import PropertyListCreateAPIView

# urlpatterns = [
#     path('properties/', PropertyListCreateAPIView.as_view(), name='property-list-create'),
# ]
# # from django.urls import path
# # from .views import PropertyListCreateAPIView, home

# # urlpatterns = [
# #     path('', home),  # Root URL
# #     path('properties/', PropertyListCreateAPIView.as_view(), name='property-list-create'),
# # ]

# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from .views import PropertyViewSet

# router = DefaultRouter()
# router.register(r'properties', PropertyViewSet, basename='property')

# urlpatterns = [
#     path('', include(router.urls)),
# ]

from django.urls import path
from .views import PropertyViewSet

urlpatterns = [
    path('properties/', PropertyViewSet.as_view({'get': 'list', 'post': 'create'}), name='property-list'),
    path('properties/<int:pk>/', PropertyViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='property-detail'),
    path('properties/all/', PropertyViewSet.as_view({'get': 'get_all_properties'}), name='property-all'),
    path('properties/drafts/', PropertyViewSet.as_view({'get': 'get_drafts'}), name='property-drafts'),
    path('properties/approved/', PropertyViewSet.as_view({'get': 'get_approved_properties'}), name='property-approved'),
    path('properties/pending/', PropertyViewSet.as_view({'get': 'get_pending'}), name='property-pending'),
    path('properties/waiting/', PropertyViewSet.as_view({'get': 'get_waiting_for_finance_properties'}), name='property-waiting'),
    path('properties/rejected/', PropertyViewSet.as_view({'get': 'get_rejected_properties'}), name='property-rejected'),
    path('properties/pending_finance/', PropertyViewSet.as_view({'get': 'get_pending_finance'}), name='property-finance-not-entered'),
    path('properties/finance_entered/', PropertyViewSet.as_view({'get': 'get_entered_finance'}), name='property-finance-entered'),
]
