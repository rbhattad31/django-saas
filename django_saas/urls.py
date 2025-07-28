"""
URL configuration for django_saas project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include,re_path
from django.conf import settings
from django.conf.urls.static import static
from Rental_Deal.views import *
from Rental_Deal import views
from django.contrib.auth.views import LogoutView

# Import the missing view functions
from Rental_Deal.views import  Rental_DealViewSet_update, Rental_DealViewSet_delete, Rental_DealViewSet_view,Rental_DealViewSet_finance_update,Rental_DealViewSet_tenancey_contact  

from Rental_Deal import urls 
from core import urls
urlpatterns = [
    path('', index, name='home'),
    path('admin/', admin.site.urls),
    path('api/', include('Rental_Deal.urls')),
    path('', include('Sales_Deals_Management.urls')),
    path('third_party_receipts/', include('Third_Party_Receipts.urls')),
    path('receipt/',include('core.urls')),
    path("rental/filter",views.Rental_DealViewSet_filter),
    path('login/', login_view, name="login"),
    path('register/', register_user, name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path('rental-deals/list/', views.all_rental_deals, name='rental-deal-list'),
    path('rental-deals/draft/', views.all_rental_deals, name='rental-deal-draft'),
    path('rental-deals/approved/', views.all_rental_deals, name='rental-deal-approved'),
    path('rental-deals/rejected/', views.all_rental_deals, name='rental-deal-rejected'),
    path('rental-deals/pending/', views.all_rental_deals, name='rental-deal-pending'),
    path('rental-deals/waiting/', views.all_rental_deals, name='rental-deal-waiting'),
    path('rental-deals/entered-finance/', views.all_rental_deals, name='rental-deal-entered-finance'),
    path('rental-deals/pending-finance/', views.all_rental_deals, name='rental-deal-pending-finance'),
    
    
    path('rental-deals/<int:pk>/delete/', Rental_DealViewSet_delete, name='rental-deal-delete'),
    path('rental-deals/view/<int:pk>/', Rental_DealViewSet_view, name='rental-deal-view'),


    path('rental-deals/update/<int:pk>/', views.edit_rental_deal_view, name='rental-deal-custom-update'),
    # path('rental-deals/upload/',  views.temp_upload_file, name='upload'),
    # path('rental-deals/delete-temp-file/', views.delete_temp_file, name='delete-temp-file'),

    path('update-single-field/', Rental_DealViewSet_finance_update, name = 'update_single_field'),
    path('api/agents/dropdown/',Rental_DealViewSet_agent_dropdown, name = 'agent-dropdown'),
    path('api/receipts/dropdown/' ,Rental_DealViewSet_receipts_dropdown,name =  'reciept-dropdown' ),
    path('rental-deals-form/', create_rental_deal_view, name = 'create-rental-deal'),


    path("tenancey/contract/download/<int:pk>/",Rental_DealViewSet_tenancey_contact,name = "tenancey-contact"),
     # Include the Rental_Deal app URLs

 

    # Matches any html file
    re_path(r'^.*\.*', pages, name='pages'),
    
    
] 

if settings.DEBUG:
    urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + urlpatterns