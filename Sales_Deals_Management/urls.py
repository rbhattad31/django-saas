from django.urls import path
from . import views
from .views import SalesDealViewSet
from django.urls import path
from .views import login_view,register_user,create_sales_deal_page
from django.contrib.auth.views import LogoutView
from .views import index


# urlpatterns = [
#     path('sales-deals/filter/', SalesDealViewSet.as_view({'post': 'datatable_filter'}), name='sales-deals-filter'),
#     path('sales-deals/', SalesDealViewSet.as_view({'get': 'list', 'post': 'create'}), name='sales-deals-list-create'),
#     # path('sales-deals/<int:pk>/', SalesDealViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='sales-deals-detail'),
#     path('sales-deals/view/<int:pk>/', SalesDealViewSet.as_view({'get': 'view_sales_deal'}), name='sales-deals-view'),
#     path('sales-deals/update/<int:pk>/', SalesDealViewSet.as_view({'post': 'update_sales_deal', "get":"update_sales_deal"}), name='sales-deals-update'),
#     path('login/', login_view, name="login"),
#     path('register/', register_user, name="register"),
#     path("logout/", LogoutView.as_view(), name="logout"),

#     path('sales-deals/<int:pk>/delete/', SalesDealViewSet.as_view({'delete': 'delete_sales'}), name='sales-deals-delete'),
#     # path('sales-deals/create/<int:pk>/', SalesDealViewSet.as_view({'post': 'create_sales_deal'}), name='sales-deals-create'),

#     path('sales-deals/create/', create_sales_deal_page, name='sales-deals-create-page'),

#     path('sales-deals/list/', views.all_sales_deals, name='Sales-deal'),
#     path('sales-deals/draft/', views.all_sales_deals, name='Sales-deal-draft'),
#     path('sales-deals/approved/', views.all_sales_deals, name='Sales-deal-approved'),
#     path('sales-deals/rejected/', views.all_sales_deals, name='Sales-deal-rejected'),
#     path('sales-deals/pending/', views.all_sales_deals, name='Sales-deal-pending'),
#     path('sales-deals/waiting/', views.all_sales_deals, name='Sales-deal-waiting'),
#     path('sales-deals/pending-finance/', views.all_sales_deals, name='Sales-deal-pending-finance'),
#     path('sales-deals/entered-finance/', views.all_sales_deals, name='Sales-deal-entered-finance'),
# ]
# urlpatterns = [
#     path('', index, name='home'),  # ✅ Fix root path for LOGIN_REDIRECT_URL = '/'

#     path('sales-deals/filter/', SalesDealViewSet.as_view({'post': 'datatable_filter'}), name='sales-deals-filter'),
#     path('sales-deals/', SalesDealViewSet.as_view({'get': 'list', 'post': 'create'}), name='sales-deals-list-create'),
#     path('sales-deals/view/<int:pk>/', SalesDealViewSet.as_view({'get': 'view_sales_deal'}), name='sales-deals-view'),
#     path('sales-deals/update/<int:pk>/', SalesDealViewSet.as_view({'post': 'update_sales_deal', "get":"update_sales_deal"}), name='sales-deals-update'),

#     path('login/', login_view, name="login"),
#     path('register/', register_user, name="register"),
#     path("logout/", LogoutView.as_view(), name="logout"),

#     path('sales-deals/<int:pk>/delete/', SalesDealViewSet.as_view({'delete': 'delete_sales'}), name='sales-deals-delete'),
#     path('sales-deals/create/', create_sales_deal_page, name='sales-deals-create-page'),

#     path('sales-deals/list/', views.all_sales_deals, name='Sales-deal'),
#     path('sales-deals/draft/', views.all_sales_deals, name='Sales-deal-draft'),
#     path('sales-deals/approved/', views.all_sales_deals, name='Sales-deal-approved'),
#     path('sales-deals/rejected/', views.all_sales_deals, name='Sales-deal-rejected'),
#     path('sales-deals/pending/', views.all_sales_deals, name='Sales-deal-pending'),
#     path('sales-deals/waiting/', views.all_sales_deals, name='Sales-deal-waiting'),
#     path('sales-deals/pending-finance/', views.all_sales_deals, name='Sales-deal-pending-finance'),
#     path('sales-deals/entered-finance/', views.all_sales_deals, name='Sales-deal-entered-finance'),
# ]


from django.urls import path
from . import views
from .views import (
    SalesDealViewSet,
    login_view,
    register_user,
    create_sales_deal_page,
    index,
)
from django.contrib.auth.views import LogoutView

urlpatterns = [
    # 👇 This will handle '/' after login
    # path('', index, name='home'),

    # Sales Deals API endpoints
    path('sales-deals/filter/', SalesDealViewSet.as_view({'post': 'datatable_filter'}), name='sales-deals-filter'),
    path('sales-deals/', SalesDealViewSet.as_view({'get': 'list', 'post': 'create'}), name='sales-deals-list-create'),
    path('sales-deals/view/<int:pk>/', SalesDealViewSet.as_view({'get': 'view_sales_deal'}), name='sales-deals-view'),
    path('sales-deals/update/<int:pk>/', SalesDealViewSet.as_view({'post': 'update_sales_deal', 'get': 'update_sales_deal'}), name='sales-deals-update'),
    path('sales-deals/<int:pk>/delete/', SalesDealViewSet.as_view({'delete': 'delete_sales'}), name='sales-deals-delete'),
    path('sales-deals/create/', create_sales_deal_page, name='sales-deals-create-page'),

    # Sales Deals List Views
    path('sales-deals/list/', views.all_sales_deals, name='Sales-deal'),
    path('sales-deals/draft/', views.all_sales_deals, name='Sales-deal-draft'),
    path('sales-deals/approved/', views.all_sales_deals, name='Sales-deal-approved'),
    path('sales-deals/rejected/', views.all_sales_deals, name='Sales-deal-rejected'),
    path('sales-deals/pending/', views.all_sales_deals, name='Sales-deal-pending'),
    path('sales-deals/waiting/', views.all_sales_deals, name='Sales-deal-waiting'),
    path('sales-deals/pending-finance/', views.all_sales_deals, name='Sales-deal-pending-finance'),
    path('sales-deals/entered-finance/', views.all_sales_deals, name='Sales-deal-entered-finance'),

    # Auth views
    path('login/', login_view, name="login"),
    path('register/', register_user, name="register"),
    path("logout/", LogoutView.as_view(next_page='/login/'), name="logout"),
]

# urlpatterns = [
#     path('source-details/', source_details_list, name='source-details-list'),
#     path('source-details/<int:pk>/', source_details_detail, name='source-details-detail'),
# ]


    
    