


from django.urls import path
from .views import role_managementlist_html , role_management_create,role_management_update,role_management_view,Role_list_view, Role_create_view , Role_retrieve_view ,Role_update_view ,  Role_partial_update_view,  Role_delete_view,Role_filter




urlpatterns = [
  path("list/" ,role_managementlist_html, name = "role-list" ),
  path("create/" , role_management_create, name = "role-create"),
  path("edit/<int:pk>/", role_management_update,name = "role-update"),
  path("view/<int:pk>/", role_management_view,name = "role-view"),
  path("filter/", Role_filter , name= "filter"),
   path('api/list/', Role_list_view, name='group-list'),
    path('api/create/', Role_create_view, name='group-create'),
    path('api/<int:pk>/', Role_retrieve_view, name='group-retrieve'),
    path('api/<int:pk>/update/', Role_update_view, name='group-update'),
    path('api/<int:pk>/partial-update/', Role_partial_update_view, name='group-partial-update'),
    path('api/<int:pk>/delete/', Role_delete_view, name='group-delete'),
   
]











