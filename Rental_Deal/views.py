from django.shortcuts import render


# Create your views here.
 
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Rental_Deal
from .serializers import DealSerializer
from rest_framework.pagination import PageNumberPagination  
from django_filters.rest_framework import DjangoFilterBackend
   

# from django_filters import rest_framework as filters

 

class Rental_DealViewSet(viewsets.ModelViewSet):
    queryset = Rental_Deal.objects.all().order_by('-created_at')
    serializer_class = DealSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = PageNumberPagination  # Use pagination for the viewset
    pagination_class.page_size = 2  # Set the default page size# Allow clients to set page size via query parameter
    pagination_class.page_size_query_param = 'size'  # Description for the page size query parameter
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
    'reference_number',
    'building_name',
    'owner_name',
    'owner_mobile',
    'deal_type',  # Assuming your model uses this name
    'deal_start_date',
    'unit_number',
    'project_name',
    'tenant_name',
    'tenant_mobile',
    'approval_status',
    'deal_end_date', 
]




    def perform_create(self, serializer):
        serializer.save()
    

    def get_queryset_submitted(self):
        Query_set = Rental_Deal.objects.filter(status='submitted').order_by('-created_at')
        print ("Query_set:", Query_set)
        return Query_set
    

    def get_queryset(self): 
        return Rental_Deal.objects.filter(agent=self.request.user)
         
    
    @action(detail=False, methods=['get'], url_path='all')
    def get_all_deals(self, request):
        # Unfiltered — return all deals
        all_deals = Rental_Deal.objects.filter(status = "submitted").order_by('created_at')
        serializer = self.get_serializer(all_deals, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='drafts')
    def get_drafts(self, request):
        drafts = self.get_queryset().filter(status='draft')
        serializer = self.get_serializer(drafts, many=True)
        return Response(serializer.data)
    

    @action(detail=False, methods=['get'], url_path='submitted')
    def get_submitted(self, request):
        submitted = Rental_Deal.objects.filter(status='submitted')
        serializer = self.get_serializer(submitted, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='approved')
    def get_approved(self, request):
        approved = self.get_queryset_submitted().filter(approval_status='approve')
        serializer = self.get_serializer(approved, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='rejected')
    def get_rejected(self, request):
        print("Fetching rejected deals")
        self.get_queryset_submitted()
        rejected =  self.get_queryset_submitted().filter(approval_status='reject')
        print("Rejected deals fetched:", rejected)
        serializer = self.get_serializer(rejected, many=True)
        return Response(serializer.data)    
    
    @action(detail=False, methods=['get'], url_path='pending')
    def get_pending(self, request):
        pending = self.get_queryset_submitted().filter(approval_status='pending')
        serializer = self.get_serializer(pending, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='wating')
    def get_wating(self, request):    
        wating = self.get_queryset_submitted().filter(approval_status='waiting')
        serializer = self.get_serializer(wating, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='finance_entered')
    def get_finance_entered(self, request):
        finance_entered = self.get_queryset_submitted().filter(is_entered_finance=True)
        serializer = self.get_serializer(finance_entered, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='finance_not_entered')
    def get_finance_not_entered(self, request):
        finance_not_entered = self.get_queryset_submitted().filter(is_entered_finance=False)
        serializer = self.get_serializer(finance_not_entered, many=True)
        return Response(serializer.data)


Rental_DealViewSet_list = Rental_DealViewSet.as_view({'get': 'list',})
Rental_DealViewSet_detail = Rental_DealViewSet.as_view({'get': 'retrieve'})
Rental_DealViewSet_create = Rental_DealViewSet.as_view({'post': 'create'})
Rental_DealViewSet_update = Rental_DealViewSet.as_view({'put': 'update','get': 'retrieve'})
Rental_DealViewSet_partial_update = Rental_DealViewSet.as_view({'patch': 'partial_update'})
Rental_DealViewSet_destroy = Rental_DealViewSet.as_view({'delete': 'destroy'})
Rental_DealViewSet_drafts = Rental_DealViewSet.as_view({'get': 'get_drafts'})
Rental_DealViewSet_submitted = Rental_DealViewSet.as_view({'get': 'get_submitted'})
Rental_DealViewSet_all = Rental_DealViewSet.as_view({'get': 'get_all_deals'}) 
Rental_DealViewSet_approved = Rental_DealViewSet.as_view({'get': 'get_approved'})
Rental_DealViewSet_rejected = Rental_DealViewSet.as_view({'get': 'get_rejected'})
Rental_DealViewSet_pending = Rental_DealViewSet.as_view({'get': 'get_pending'})
Rental_DealViewSet_wating = Rental_DealViewSet.as_view({'get': 'get_wating'})
 # 👈 this line
# finace enterd
Rental_DealViewSet_finance_entered = Rental_DealViewSet.as_view({'get': 'get_finance_entered'})
Rental_DealViewSet_finance_not_entered = Rental_DealViewSet.as_view({'get': 'get_finance_not_entered'})
