from django.urls import path
from .views import DepositsViewSet, third_party_receipts_page, DepositsViewSet_filter
from .views import (
    third_party_receipts_page,
    DepositsViewSet_filter,
)

urlpatterns = [
    path('list/', third_party_receipts_page, name='third_party_receipts_list'),
    path('api/deposits/filter/', DepositsViewSet_filter, name='deposits_filter'),
    path('third-party/view/<int:pk>/', DepositsViewSet.as_view({'get': 'view_third_party'}), name='third-party-view'),
    path('third-party/update/<int:pk>/', DepositsViewSet.as_view({'get': 'update_third_party'}), name='third-party-update'),

]
