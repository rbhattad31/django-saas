 


from django.urls import path
from . import views
from .views import   Rental_PropertyViewSet
from .views import PropertyAPIView, edit_property_page
from django.contrib.auth.views import LogoutView
from .views import rental_property_create, draft_property_list,ManagementReceiptsViewSet,edit_management_receipt

management_receipts_view = ManagementReceiptsViewSet.as_view({'get': 'view_receipt'})


urlpatterns = [
    # Rental Deal URLs
    # path('', views.dashboard_view, name='dashboard'),
    path('rental-properties/filter/', views.Rental_PropertyViewSet_filter, name='rental-property-filter'),
    path('rental-properties/<int:pk>/view/', Rental_PropertyViewSet.as_view({'get': 'view_property'}), name='rental-property-view'),
    path('rental-properties/<int:pk>/', Rental_PropertyViewSet.as_view({'put': 'update'}), name='rental-property-update'),
    path('rental-properties/<int:pk>/edit/', views.edit_property_page, name='rental-property-edit'),
    path('api/rental-properties/<int:pk>/', PropertyAPIView.as_view(), name='property-api'),
    # path('management_receipts/downloadReceiptPDF/<int:pk>/', views.download_receipt, name='download-receipt'),
    path('rental-properties/<int:pk>/delete/', Rental_PropertyViewSet.as_view({'delete': 'delete_property'}), name='rental-property-delete'),
    path('rental-properties/create-form/', Rental_PropertyViewSet.as_view({'get': 'create_form'}), name='rental-property-create-form'),
    path('rental-properties/create/', Rental_PropertyViewSet.as_view({'post': 'create'}), name='rental-property-create'),
    path('api/agents/dropdown/', Rental_PropertyViewSet.as_view({'get': 'submitted_by_user_dropdown'}), name='agent-dropdown'),
    # path('login/', login_view, name="login"),
    # path('register/', register_user, name="register"),
    # path("logout/", LogoutView.as_view(), name="logout"),
    path('rental-properties/list/', views.all_rental_properties, name='rental-property-list'),
    path('rental-properties/draft/', views.all_rental_properties, name='rental-property-draft'),
    path('rental-properties/approved/', views.all_rental_properties, name='rental-property-approved'),
    path('rental-properties/rejected/', views.all_rental_properties, name='rental-property-rejected'),
    path('rental-properties/pending/', views.all_rental_properties, name='rental-property-pending'),
    path('rental-properties/waiting/', views.all_rental_properties, name='rental-property-waiting'),
    path('rental-properties/entered-finance/', views.all_rental_properties, name='rental-property-entered-finance'),
    path('rental-properties/waiting-finance/', views.all_rental_properties, name='rental-property-waiting-finance'),
    path('property/create/', rental_property_create, name='rental-property-create'),
    path('save-draft/', rental_property_create, name='save-draft'),
    path('draft-properties/', views.draft_property_list, name='draft-property-list'),

    # New URL to handle PUT requests explicitly for file updates
    path('api/rental-properties/<int:pk>/update/', Rental_PropertyViewSet.as_view({'put': 'update'}), name='rental-property-update-api'),
    path(
        'management-receipts/managerdatatablefilter/',
        ManagementReceiptsViewSet.as_view({'post': 'managerdatatablefilter'}),
        name='managerdatatablefilter'
    ),

    path('management-receipts/managerdatatablefilter/', ManagementReceiptsViewSet.as_view({'post': 'managerdatatablefilter'}), name='managerdatatablefilter'),

    # New URLs for Management Receipts
    path('management-receipts/', views.management_receipts_manager, name='management_receipts_manager'),
    path('management-receipts/create/', ManagementReceiptsViewSet.as_view({'post': 'create_receipt'}), name='management_receipts_create'),
    # path('management-receipts/<int:pk>/edit/', ManagementReceiptsViewSet.as_view({'put': 'edit_receipt'}), name='management_receipts_edit'),
    path('management-receipts/<int:pk>/edit-receipt/', ManagementReceiptsViewSet.as_view({'get': 'edit_receipt', 'post': 'edit_receipt'}), name='management_receipts_edit_receipt'),    # path('management-receipts/<int:pk>/view/', ManagementReceiptsViewSet.as_view({'get': 'view_receipt'}), name='management_receipts_view'),
    path('management-receipts/<int:pk>/downloadReceiptPDF/', ManagementReceiptsViewSet.as_view({'get': 'download_receipt'}), name='download-receipt'),
    path('management-receipts/<int:pk>/view-receipt/', ManagementReceiptsViewSet.as_view({'get': 'view_receipt'}), name='management_receipts_view'),
    path('api/management-receipts/<int:pk>/edit/', ManagementReceiptsViewSet.as_view({
        'get': 'edit_management',
        'put': 'update'
    }), name='management_receipts_edit'),
    path('management-receipts/create-form/', ManagementReceiptsViewSet.as_view({'get': 'create_form'}), name='management_receipts_create_form'),
    path('management-receipts/create/', ManagementReceiptsViewSet.as_view({'post': 'create_receipt'}), name='management_receipts_create'),

]