from django.urls import path
from . import views

urlpatterns = [
    # Rental Deal URLs
    
    # path('rental-deals/create/', views.Rental_DealViewSet_create, name='rental-deal-create'),
 
    path('rental-deals/filter/', views.Rental_DealViewSet_filter, name='rental-deal-filter'),
   
]
