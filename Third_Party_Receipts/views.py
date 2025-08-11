from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.response import Response
from django.db.models import Q
from core.models import Deposits
from rest_framework.decorators import action
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.template.loader import render_to_string
from .serializers import DepositsSerializer, DepositsfilterSerializer
from weasyprint import HTML

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
        serializer = DepositsSerializer(deposit,context = {'request': request})
        aws_url = settings.AWS_URL  # optional, include if you use S3

        return render(request, 'viewThird_Party.html', {
            'deposit': serializer.data,
            'aws_base_url': aws_url
        })
    

    @action(detail=False, methods=['get', 'post'], url_path='update')
    def update_third_party(self, request, pk=None):
        deposit = get_object_or_404(Deposits, pk=pk)
        serializer = DepositsSerializer(deposit, partial=True  ,context = {'request': request})

        return render(request, 'editThird_Party.html', {
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

        serializer = DepositsSerializer(paginated, many=True , context = {'request': request})
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
    return render(request, 'Third_Party_Receipts.html')





def download_receipt_pdf(request, receipt_id):
    receipt = Deposits.objects.get(id=receipt_id)
    html_string = render_to_string('recicepts_pdf.html', {'receipt': receipt})
    html = HTML(string=html_string, base_url=request.build_absolute_uri('/'))
    pdf_file = html.write_pdf()

    download = request.GET.get("download") == "1"
    disposition = 'attachment' if download else 'inline'

    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'{disposition}; filename="receipt_{receipt.deposit_number}.pdf"'
    return response
