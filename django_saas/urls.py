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
from Rental_Deal.views import index, pages, login_view, register_user, all_rental_deals
from Rental_Deal import views
from django.contrib.auth.views import LogoutView

from Rental_Deal import urls 

urlpatterns = [
    path('', index, name='home'),
    path('admin/', admin.site.urls),
    path('api/', include('Rental_Deal.urls')),
    path('login/', login_view, name="login"),
    path('register/', register_user, name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
     path('rental-deals/all/', views.all_rental_deals, name='rental-deal'),
    path('rental-deals/draft/', views.all_rental_deals, name='rental-deal-draft'),
    path('rental-deals/approved/', views.all_rental_deals, name='rental-deal-approved'),
    path('rental-deals/rejected/', views.all_rental_deals, name='rental-deal-rejected'),
    path('rental-deals/pending/', views.all_rental_deals, name='rental-deal-pending'),
    path('rental-deals/waiting/', views.all_rental_deals, name='rental-deal-waiting'),
    path('rental-deals/entered-finance/', views.all_rental_deals, name='rental-deal-entered-finance'),
    path('rental-deals/waiting-finance/', views.all_rental_deals, name='rental-deal-waiting-finance'),

     # Include the Rental_Deal app URLs

    # Removed path('', views.index, name='home') because 'views' is not defined

    # Matches any html file
    re_path(r'^.*\.*', pages, name='pages'),
    
    # path('silk/', include('silk.urls', namespace='silk'))
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)