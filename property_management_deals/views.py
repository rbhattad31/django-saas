
# views.py
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from .models import Property
from rest_framework.response import Response
from .serializers import PropertySerializer
from django_filters.rest_framework import DjangoFilterBackend


class PropertyPagination(PageNumberPagination):
    page_size = 1    # Number of items per page
    page_size_query_param = 'page_size'  # Client can set custom page size with ?page_size=
    max_page_size = 50 
class PropertyViewSet(ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [permissions.IsAuthenticated] 
    pagination_class = PropertyPagination  # Enable pagination here
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['reference_number','building_name','pm_start_date','tenancy_start_date', 'deal_date','unit_no','project_name','pm_end_date','tenancy_end_date','approval_status','Form_status']



    def perform_create(self, serializer):
        serializer.save()

    def get_queryset_submitted(self):
        return Property.objects.filter(Form_status='Submitted').order_by('deal_date')

    def get_queryset(self): 
        return Property.objects.filter(agent_name=self.request.user)

    @action(detail=False, methods=['get'], url_path='all')
    def get_all_properties(self, request):
        all_props = Property.objects.filter(Form_status="Submitted").order_by('deal_date')
        serializer = self.get_serializer(all_props, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='drafts')
    def get_drafts(self, request):
        drafts = self.get_queryset().filter(Form_status='Draft')
        serializer = self.get_serializer(drafts, many=True)
        return Response(serializer.data)

    # @action(detail=False, methods=['get'], url_path='submitted')
    # def get_submitted(self, request):
    #     submitted = Property.objects.filter(status='submitted')
    #     serializer = self.get_serializer(submitted, many=True)
    #     return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='approved')
    def get_approved_properties(self, request):
        approved = self.get_queryset_submitted().filter(approval_status='Accept')
        serializer = self.get_serializer(approved, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='pending')
    def get_pending(self, request):
        pending = self.get_queryset_submitted().filter(approval_status='Pending')
        serializer = self.get_serializer(pending, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='waiting')
    def get_waiting_for_finance_properties(self, request):
        waiting = self.get_queryset_submitted().filter(approval_status='Waiting for Finance')
        serializer = self.get_serializer(waiting, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='rejected')
    def get_rejected_properties(self, request):
        rejected = self.get_queryset_submitted().filter(approval_status='Reject')
        serializer = self.get_serializer(rejected, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='finance_not_entered')
    def get_pending_finance(self, request):
        finance_not_entered = self.get_queryset_submitted().filter(is_entered_finance=False)
        serializer = self.get_serializer(finance_not_entered, many=True)
        return Response(serializer.data)
   

    @action(detail=False, methods=['get'], url_path='finance_entered')
    def get_entered_finance(self, request):
        finance_entered = self.get_queryset_submitted().filter(is_entered_finance=True)
        serializer = self.get_serializer(finance_entered, many=True)
        return Response(serializer.data)

   

