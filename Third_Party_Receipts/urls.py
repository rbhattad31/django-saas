from django.urls import path
from .views import DepositsViewSet, third_party_receipts_page,thrid_party_recipt_crete_htmlpage, DepositsViewSet_filter,DepositsViewSet_create,DepositsViewSet_edit
from .views import (
    third_party_receipts_page,
    DepositsViewSet_filter,
) 
from .views import download_receipt_pdf

urlpatterns = [
    path('list/', third_party_receipts_page, name='third_party_receipts_list'),
    path('api/deposits/filter/', DepositsViewSet_filter, name='deposits_filter'),
    path('api/deposits/create/',  DepositsViewSet_create, name='deposits_create'),
    path("api/deposits/edit/" , DepositsViewSet_edit , name = "deposits-edit"),
    

    path('create/' , thrid_party_recipt_crete_htmlpage , name = "create-page" ),
    path('third-party/view/<int:pk>/', DepositsViewSet.as_view({'get': 'view_third_party'}), name='third-party-view'),
    path('third-party/update/<int:pk>/', DepositsViewSet.as_view({'get': 'update_third_party'}), name='third-party-update'),
    path("recipts/download/<int:receipt_id>/", download_receipt_pdf, name='download_receipt_pdf'),

]
