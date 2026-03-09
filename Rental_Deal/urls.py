from django.urls import path
from . import views

urlpatterns = [
    # Rental Deal URLs
    
    # path('rental-deals/create/', views.Rental_DealViewSet_create, name='rental-deal-create'),
 
    path('rental-deals/filter', views.Rental_DealViewSet_filter, name='rental-deal-filter'),
    path('rental-deals/update/<int:pk>/', views.Rental_DealViewSet_update, name='rental-deal-update'),
    path('rental-deals/create/', views.Rental_DealViewSet_create, name='rental-deal-create'),
    path('rental-deals/edit_reference_number/<int:pk>/', views.Rental_DealViewSet_clone, name='rental-deal-clone'),

]
