import json
from django.http import HttpResponse
from rest_framework import viewsets , status
from rest_framework.response import Response
from django.db.models import Q
from core.models import Deposits  , Users
from  Rental_Deal.serializers import AgentDropdownSerializer
from rest_framework.decorators import action, permission_classes
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.template.loader import render_to_string
from .serializers import Deposits_create_Serializer, DepositsSerializer, DepositsfilterSerializer
from weasyprint import HTML
from rest_framework.permissions import BasePermission
from django.contrib.auth.decorators import login_required, permission_required

class CanViewTrhidpartyRecipts(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm("core.view_deposits")
    
class CanChangeTrhidpartyRecipts(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm("core.chanage_deposits")

class DepositsViewSet(viewsets.ModelViewSet):
    queryset = Deposits.objects.all().order_by('-id')
    # serializer_class = DepositsSerializer
    def get_serializer_class(self):
        if self.action == 'datatable_filter':
            return DepositsfilterSerializer
        return DepositsSerializer

    @action(detail=True, methods=['get'], url_path='view' )
    @permission_classes([CanViewTrhidpartyRecipts ]) 
    def view_third_party(self, request, pk=None):
        deposit = get_object_or_404(Deposits, pk=pk)
        serializer = DepositsSerializer(deposit,context = {'request': request})
        aws_url = settings.AWS_URL  # optional, include if you use S3

        print(serializer.data)

        return render(request, 'viewThird_Party.html', {
            'deposit': serializer.data,
            'aws_base_url': aws_url
        })
    





    @action(detail=False, methods=['post'], url_path='filter')
    def datatable_filter(self, request):
        if not request.user.has_perm("core.list_third_party_deposits"):
            return Response({"detail": "You do not have permission to access this."}, status=status.HTTP_403_FORBIDDEN)
        print("Request Data:", request.data)  # Debugging line
        data = DepositsfilterSerializer(data=request.data)
        data.is_valid(raise_exception=True)
        validated = data.validated_data
        print("Validated Data:", validated) 

        account_id = request.user.account_id

        queryset = Deposits.objects.filter(account_id = account_id).order_by("-id")
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
    


    # create the deposits api view
    @action(detail= False , method = ["post"] , url_path = "create")
    def create_thrid_party_recicept(self,request):
        if not request.user.has_perm("core.add_deposits"):
            return Response({"detail": "You do not have permission to access this."}, status=status.HTTP_403_FORBIDDEN)
        print(request.data)
        print(request.user.account_id)
        mutable_data = request.data.copy()

        deposit_number = request.data.get("deposit_number")
        print(request.data)
        mutable_data  = request.data.copy()

        if  Deposits.objects.filter(deposit_number=deposit_number).exists():
            return Response(
                {"error": f"Receipt number {deposit_number} is already taken."},
                status=status.HTTP_400_BAD_REQUEST
            )

        mutable_data['account_id'] = request.user.account_id
        mutable_data['mail_status'] = "sent"
        mutable_data['status'] = ""
    

        print(mutable_data , "mutable data is  ")




        serializer = Deposits_create_Serializer(data=mutable_data )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

      
    
    # edit the deposite or thritd party recipts
    @action(detail=False, methods=['get', 'post'], url_path='update')
    @permission_classes([CanChangeTrhidpartyRecipts])
    def update_third_party(self, request, pk=None):
        if not request.user.has_perm("core.change_deposits"):
            return Response({"detail": "You do not have permission to access this."}, status=status.HTTP_403_FORBIDDEN)
        if request.method  =="GET":
            deposit = get_object_or_404(Deposits, pk=pk)
            serializer = DepositsSerializer(deposit ,context = {'request': request})

            return render(request, 'editThird_Party.html', {
                'deposit': serializer.data
            })
        elif request.method == "PUT":
            # deposit = get_object_or_404(Deposits, pk=pk)
            
            # mutable_data = request.data.copy()

            # print(mutable_data)
           



            # serializer = DepositsSerializer( instance=deposit, data = mutable_data ,partial=True  ,context = {'request': request})
            # if serializer.is_valid():
            #     serializer.save()
            #     return Response(serializer.data, status=status.HTTP_200_OK)
            # else:
            #     return Response("not valid form " , status= status.HTTP_400_BAD_REQUEST)
            print(pk)
            deposit = get_object_or_404(Deposits, pk=pk)

            mutable_data = request.data.copy()
            print(mutable_data)

            serializer = DepositsSerializer(
                instance=deposit,
                data=mutable_data,
                partial=True,
                context={'request': request}
            )

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            










DepositsViewSet_filter =  DepositsViewSet.as_view({
    'post': 'datatable_filter'
})
DepositsViewSet_create = DepositsViewSet.as_view({ "post" : "create_thrid_party_recicept"})
DepositsViewSet_edit = DepositsViewSet.as_view({'put' : "update_third_party"})

@login_required(login_url="/login/")
@permission_required('core.list_third_party_deposits',raise_exception=True)
def third_party_receipts_page(request):
    return render(request, 'Third_Party_Receipts.html')




@login_required(login_url="/login/")
@permission_required('core.download_third_party_deposits',raise_exception=True)
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


@login_required(login_url="/login/")
@permission_required('core.list_third_party_deposits',raise_exception=True)
def thrid_party_recipt_crete_htmlpage(request):
    return render(request , "createThird_Party.html")

#serving the  create html page
@login_required(login_url="/login/")
@permission_required('core.add_deposits',raise_exception=True)
def thrid_party_recipt_crete_htmlpage(request):
    latest = Deposits.objects.order_by('-deposit_number').first()
    next_receipt = int(latest.deposit_number) + 1 if latest and latest.deposit_number else 1

    agents = Users.objects.filter(is_active=True,  account_id = request.user.account_id)
    agents = AgentDropdownSerializer(agents, many=True).data
    reciecpt_data = {
        'agents': agents
    }

    return render(request, "createThird_Party.html", {
        "next_receipt_number": next_receipt,"reciecpt_data" :  json.dumps(reciecpt_data)
    })
