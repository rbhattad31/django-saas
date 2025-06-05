from django.urls import path
from . import views

urlpatterns = [
    # Rental Deal URLs
    path('rental-deals/', views.Rental_DealViewSet_list, name='rental-deal-list'),
    path('rental-deals/<int:pk>/', views.Rental_DealViewSet_detail, name='rental-deal-detail'),
    path('rental-deals/create/', views.Rental_DealViewSet_create, name='rental-deal-create'),
    path('rental-deals/update/<int:pk>/', views.Rental_DealViewSet_update, name='rental-deal-update'),
    path('rental-deals/partial-update/<int:pk>/', views.Rental_DealViewSet_partial_update, name='rental-deal-partial-update'),
    path('rental-deals/drafts/', views.Rental_DealViewSet_drafts, name='rental-deal-drafts'),
    path('rental-deals/submitted/', views.Rental_DealViewSet_submitted, name='rental-deal-submitted'),
    path('rental-deals/delete/<int:pk>/', views.Rental_DealViewSet_destroy, name='rental-deal-delete'),
    path('rental-deals/all/', views.Rental_DealViewSet_all, name='rental-deal-all'),
    path('rental-deals/approved/', views.Rental_DealViewSet_approved, name='rental-deal-approved'),
    path('rental-deals/rejected/', views.Rental_DealViewSet_rejected, name='rental-deal-rejected'),
    path('rental-deals/pending/', views.Rental_DealViewSet_pending, name='rental-deal-pending'),
    path('rental-deals/wating/', views.Rental_DealViewSet_wating, name='rental-deal-wating'),
    path('rental-deals/finance-entered/', views.Rental_DealViewSet_finance_entered, name='rental-deal-finance-entered'),
    path('rental-deals/finance-not-entered/', views.Rental_DealViewSet_finance_not_entered, name='rental-deal-finance-not-entered'),
]
