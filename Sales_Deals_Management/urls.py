from django.urls import path
from . import views


urlpatterns = [
    path('sales-deals/', views.SalesDealViewSet_list, name='sales-deal-list'),
    path('sales-deals/<int:pk>/', views.SalesDealViewSet_detail, name='sales-deal-detail'),
    path('sales-deals/create/', views.SalesDealViewSet_create, name='sales-deal-create'),
    path('sales-deals/update/<int:pk>/', views.SalesDealViewSet_update, name='sales-deal-update'),
    path('sales-deals/partial-update/<int:pk>/', views.SalesDealViewSet_partial_update, name='sales-deal-partial-update'),
    path('sales-deals/delete/<int:pk>/', views.SalesDealViewSet_destroy, name='sales-deal-delete'),
    
    # Custom filtered views
    path('sales-deals/drafts/', views.SalesDealViewSet_drafts, name='sales-deal-drafts'),
    path('sales-deals/submitted/', views.SalesDealViewSet_submitted, name='sales-deal-submitted'),
    path('sales-deals/approved/', views.SalesDealViewSet_approved, name='sales-deal-approved'),
    path('sales-deals/rejected/', views.SalesDealViewSet_rejected, name='sales-deal-rejected'),
    path('sales-deals/pending/', views.SalesDealViewSet_pending, name='sales-deal-pending'),
    path('sales-deals/waiting/', views.SalesDealViewSet_waiting, name='sales-deal-waiting'),
    path('sales-deals/finance-entered/', views.SalesDealViewSet_finance_entered, name='sales-deal-finance-entered'),
    path('sales-deals/finance-not-entered/', views.SalesDealViewSet_finance_not_entered, name='sales-deal-finance-not-entered'),
]



# urlpatterns = [
#     path('source-details/', source_details_list, name='source-details-list'),
#     path('source-details/<int:pk>/', source_details_detail, name='source-details-detail'),
# ]