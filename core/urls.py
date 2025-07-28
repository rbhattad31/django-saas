from django.urls import path
from . import views

urlpatterns = [
    
 
    path('list/',views.reciept_table_view, name = "receipts_list"),
    path("api/filter/", views.Receipts_Viewset_filter,name= "receipts_filter"),
    path('create/', views.recicept_create, name="reciecpt_create_page" ),
    path('api/create/',views.Receipts_Viewset_create, name = "reciecpt_create"),
    path("view/<int:pk>/", views.recicept_view , name = "recicept_view"),
    path("api/edit/<int:pk>/", views.Receipts_ViewSet_update ,name = "recicept_edit"),
    path("edit/<int:pk>/", views.edit_recipt_deal_view ,name = "recicept_edit_page"),
    path('<int:receipt_id>/download/', views.download_receipt_pdf, name='download_receipt_pdf'),
  
    

]