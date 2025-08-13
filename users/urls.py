from django.urls import path 
from .views import filter ,UserdatafilterViewset 








 
urlpatterns = [
    path("list/" ,  filter , name = "user-list"),
    path("api/users/filter" , UserdatafilterViewset ,name = "user-filter" ),
    path("api/create/" , UserdatafilterViewset ,name = "user-create" )
    # path("view/" , ),
    # path("edit/<int:pk>/" , ),
    # path("create/" , )
]



