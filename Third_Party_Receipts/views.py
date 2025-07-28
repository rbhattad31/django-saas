from rest_framework import viewsets
from rest_framework.response import Response
from django.db.models import Q
from core.models import Deposits
from rest_framework.decorators import action
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from .serializers import DepositsSerializer, DepositsfilterSerializer

class DepositsViewSet(viewsets.ModelViewSet):
    queryset = Deposits.objects.all().order_by('-id')
    # serializer_class = DepositsSerializer
    def get_serializer_class(self):
        if self.action == 'datatable_filter':
            return DepositsfilterSerializer
        return DepositsSerializer

    @action(detail=True, methods=['get'], url_path='view')
    def view_third_party(self, request, pk=None):
        deposit = get_object_or_404(Deposits, pk=pk)
        serializer = DepositsSerializer(deposit)
        aws_url = settings.AWS_URL  # optional, include if you use S3

        return render(request, 'third_party_receipts/viewThird_Party.html', {
            'deposit': serializer.data,
            'aws_base_url': aws_url
        })
    

    @action(detail=False, methods=['get', 'post'], url_path='update')
    def update_third_party(self, request, pk=None):
        deposit = get_object_or_404(Deposits, pk=pk)
        serializer = DepositsSerializer(deposit, partial=True)

        return render(request, 'third_party_receipts/editThird_Party.html', {
            'deposit': serializer.data
        })



    @action(detail=False, methods=['post'], url_path='filter')
    def datatable_filter(self, request):
        print("Request Data:", request.data)  # Debugging line
        data = DepositsfilterSerializer(data=request.data)
        data.is_valid(raise_exception=True)
        validated = data.validated_data
        print("Validated Data:", validated) 

        queryset = Deposits.objects.all()
        print("Initial Queryset:", queryset)  # Debugging line

        # Global search
        search_term = validated.get("search", {}).get("value") or ''
        if search_term:
            queryset = queryset.filter(
                Q(deposit_number__icontains=search_term) |
                Q(date__icontains=search_term) |
                Q(dhs__icontains=search_term) |
                Q(fils__icontains=search_term) |
                Q(payment_type__icontains=search_term) |
                Q(sec_date__icontains=search_term) |
                Q(deal_type__icontains=search_term) |
                Q(agent_name__icontains=search_term) |
                Q(project_name__icontains=search_term) |
                Q(building_name__icontains=search_term) |
                Q(unit_number__icontains=search_term)
            )

            print("Search Term:", search_term)  # Debugging line
        print("Filtered Queryset:", queryset)  # Debugging line
        # Field-specific filters
        filter_fields = [
                        'id', 'deposit_number', 'date', 'dhs', 'fils', 'payment_type',
                        'sec_date', 'deal_type', 'agent_name', 'project_name', 'building_name', 'unit_number'
                    ]
        for field in filter_fields:
            value = validated.get(field)
            if value:
                filter_kwargs = {f"{field}__icontains": value}
                queryset = queryset.filter(**filter_kwargs)

        # Deal Type Filter
      

        # Date range filter
        if validated.get("from_date"):
            queryset = queryset.filter(date__gte=validated.get("from_date"))
        if validated.get("to_date"):
            queryset = queryset.filter(date__lte=validated.get("to_date"))

        # Manual Pagination for DataTables
        start = validated.get("start", 0)
        length = validated.get("length", 10)
        paginated = queryset[start:start + length]

        serializer = DepositsSerializer(paginated, many=True)
        response_data = {
            "draw": validated.get("draw", 0),
            "recordsTotal": queryset.count(),
            "recordsFiltered": queryset.count(),
            "data": serializer.data,
        }
        return Response(response_data)
    










DepositsViewSet_filter =  DepositsViewSet.as_view({
    'post': 'datatable_filter'
})


def third_party_receipts_page(request):
    return render(request, 'third_party_receipts/Third_Party_Receipts.html')
