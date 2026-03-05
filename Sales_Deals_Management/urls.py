from django.urls import path
from . import views
from .views import SalesDealViewSet, SalesDealViewSet_update, SalesDealViewset_edit_reference_number
from django.urls import path
from .views import  create_sales_deal_page , edit_sales_deal_page
from .views import Sales_DealViewSet_update_single_field, SalesDealViewSet_create
 


 


from django.urls import path
from . import views
from .views import (
    SalesDealViewSet,
 
    create_sales_deal_page,
 
)
from django.contrib.auth.views import LogoutView

urlpatterns = [
    # 👇 This will handle '/' after login
    # path('', index, name='home'),

    # Sales Deals API endpoints
    path('sales-deals/filter/', SalesDealViewSet.as_view({'post': 'datatable_filter'}), name='sales-deals-filter'),
    path('sales-deals/', SalesDealViewSet.as_view({'get': 'list', 'post': 'create'}), name='sales-deals-list-create'),
    path('sales-deals/view/<int:pk>/', SalesDealViewSet.as_view({'get': 'view_sales_deal'}), name='sales-deals-view'),
    path('api/sales-deals/update/<int:pk>/', SalesDealViewSet_update , name='sales-deals-update'),
    path('sales-deals/<int:pk>/edit/', edit_sales_deal_page, name='sales-deals-edit-page'),
    path('sales-deals/<int:pk>/delete/', SalesDealViewSet.as_view({'delete': 'delete_sales'}), name='sales-deals-delete'),
    path('sales-deals/create/', create_sales_deal_page, name='sales-deals-create-page'),
    path('api/sales-deals/create/', SalesDealViewSet_create, name='sales-deals-create'),

    # Sales Deals List Views
    path('sales-deals/list/', views.all_sales_deals, name='Sales-deal'),
    path('sales-deals/draft/', views.all_sales_deals, name='Sales-deal-draft'),
    path('sales-deals/approved/', views.all_sales_deals, name='Sales-deal-approved'),
    path('sales-deals/rejected/', views.all_sales_deals, name='Sales-deal-rejected'),
    path('sales-deals/pending/', views.all_sales_deals, name='Sales-deal-pending'),
    path('sales-deals/waiting/', views.all_sales_deals, name='Sales-deal-waiting'),
    path('sales-deals/pending-finance/', views.all_sales_deals, name='Sales-deal-pending-finance'),
    path('sales-deals/entered-finance/', views.all_sales_deals, name='Sales-deal-entered-finance'),
    path('sales-deals/update-single-field/', Sales_DealViewSet_update_single_field, name='update_single_field'),
    path('sales-deals/edit_reference_number/<int:pk>/', SalesDealViewset_edit_reference_number, name='sales-deals-edit-reference-number'),

    # Auth views
    # path('login/', login_view, name="login"),
    # path('register/', register_user, name="register"),
    # path("logout/", LogoutView.as_view(next_page='/login/'), name="logout"),
]

# urlpatterns = [
#     path('source-details/', source_details_list, name='source-details-list'),
#     path('source-details/<int:pk>/', source_details_detail, name='source-details-detail'),
# ]


    
    