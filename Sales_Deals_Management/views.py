from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from .models import SalesDeal
from rest_framework.decorators import action
from .serializers import SalesDealSerializer 

class SalesDealViewSet(viewsets.ModelViewSet):
    queryset = SalesDeal.objects.all().order_by('-created_at')
    serializer_class = SalesDealSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    pagination_class= PageNumberPagination
    pagination_class.page_size=2
    pagination_class.page_size_query_param='size'
    filterset_fields = ['reference_number', 'unit_no','building_name','project_name','seller_name','buyer_mobile','seller_source','seller_mobile','buyer_name','buyer_source','status']

    def get_queryset(self):
        return SalesDeal.objects.filter(deal_submitted_by_agent=self.request.user)


    def get_queryset_submitted(self):
        return SalesDeal.objects.filter(status='submitted').order_by('-created_at')

    @action(detail=False, methods=['get'], url_path='drafts')
    def get_drafts(self, request):
        drafts = self.get_queryset().filter(status='draft')
        page = self.paginate_queryset(drafts)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(drafts, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='submitted')
    def get_submitted(self, request):
        submitted = SalesDeal.objects.filter(status='submitted')
        page = self.paginate_queryset(submitted)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(submitted, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='approved')
    def get_approved(self, request):
        approved = self.get_queryset_submitted().filter(approval_status='approve')
        page = self.paginate_queryset(approved)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(approved, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='rejected')
    def get_rejected(self, request):
        rejected = self.get_queryset_submitted().filter(approval_status='reject')
        page = self.paginate_queryset(rejected)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(rejected, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='pending')
    def get_pending(self, request):
        pending = self.get_queryset_submitted().filter(approval_status='pending')
        page = self.paginate_queryset(pending)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(pending, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='waiting')
    def get_waiting(self, request):
        waiting = self.get_queryset_submitted().filter(approval_status='waiting')
        page = self.paginate_queryset(waiting)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(waiting, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='finance_entered')
    def get_finance_entered(self, request):
        entered = self.get_queryset_submitted().filter(is_entered_finance=True)
        page = self.paginate_queryset(entered)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(entered, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='finance_not_entered')
    def get_finance_not_entered(self, request):
        not_entered = self.get_queryset_submitted().filter(is_entered_finance=False)
        page = self.paginate_queryset(not_entered)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(not_entered, many=True)
        return Response(serializer.data)

# class SourceDetailsViewSet(viewsets.ModelViewSet):
#     queryset = SourceDetails.objects.all()
#     serializer_class = SourceDetailsSerializer



SalesDealViewSet_list = SalesDealViewSet.as_view({'get': 'list'})
SalesDealViewSet_detail = SalesDealViewSet.as_view({'get': 'retrieve'})
SalesDealViewSet_create = SalesDealViewSet.as_view({'post': 'create'})
SalesDealViewSet_update = SalesDealViewSet.as_view({'put': 'update'})
SalesDealViewSet_partial_update = SalesDealViewSet.as_view({'patch': 'partial_update'})
SalesDealViewSet_destroy = SalesDealViewSet.as_view({'delete': 'destroy'})

SalesDealViewSet_drafts = SalesDealViewSet.as_view({'get': 'get_drafts'})
SalesDealViewSet_submitted = SalesDealViewSet.as_view({'get': 'get_submitted'})
SalesDealViewSet_approved = SalesDealViewSet.as_view({'get': 'get_approved'})
SalesDealViewSet_rejected = SalesDealViewSet.as_view({'get': 'get_rejected'})
SalesDealViewSet_pending = SalesDealViewSet.as_view({'get': 'get_pending'})
SalesDealViewSet_waiting = SalesDealViewSet.as_view({'get': 'get_waiting'})
SalesDealViewSet_finance_entered = SalesDealViewSet.as_view({'get': 'get_finance_entered'})
SalesDealViewSet_finance_not_entered = SalesDealViewSet.as_view({'get': 'get_finance_not_entered'})
