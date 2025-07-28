from django.shortcuts import render
from rest_framework import viewsets, permissions
import datetime
from fileinput import filename
from urllib import request
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
import re
from weasyprint import HTML
# from .Utilities import delete_from_s3, upload_file_to_full_s3_url


# Create your views here.
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from core.models import Users
# from .forms import RentalDealForm, FinanceCommentForm


from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from core.models import RentalDeals,Users,Account,Receipts
from Rental_Deal.serializers import  AgentDropdownSerializer
# from .pagination import CustomPagination  
from rest_framework.pagination import PageNumberPagination  
# from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
# from .forms import LoginForm, SignUpForm  # Add this import for LoginForm and SignUpForm
from datetime import datetime
   

# from django_filters import rest_framework as filters
from django.template import loader
from django import template
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import Group  # Add this import
import os
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.utils.timezone import now  # Add this import
import time
import json


from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from django.db.models import Q
from rest_framework import status

from core.serializers import DataTableSearchSerializer, ReceiptSerilizer

from django.template.loader import render_to_string

from .models import Receipts

# Create your views here.


# recipts mOdel to handel Edit create view 
class Receipts_ViewSet(viewsets.ModelViewSet):
    queryset = Receipts.objects.all() # Define base queryset for the ViewSet


    def get_serializer_class(self):
        if self.action == "list":
            return DataTableSearchSerializer  # Only use this for DataTables
        return ReceiptSerilizer  # Default serializer for standard CRUD actions

    @action(detail=False, methods=['post'], url_path='filter')
    def reciecptstable_filter(self, request):
        # 1. Validate incoming request data using DataTableSearchSerializer
        print(request.data)
        serializer =  DataTableSearchSerializer(data=request.data)
        serializer.is_valid(raise_exception=True) # This will raise 400 if validation fails
        validated_data = serializer.validated_data

        # print("Validated Data:", validated_data) # Good for debugging

        # Extract standard DataTables parameters
        draw = validated_data['draw']
        start = validated_data['start']
        length = validated_data['length']

        # Extract global search term and its parsed date version
        global_search_value = validated_data.get('search', {}).get('value', '')
        global_search_date_parsed = validated_data.get('search_date_parsed') # This is a date object or None

        # Extract custom filter parameters (already cleaned by serializer)
        filter_type = validated_data.get('type')
        from_date = validated_data.get('from_date') # This is already a Python date object or None
        to_date = validated_data.get('to_date')     # This is already a Python date object or None
        receipt_number = validated_data.get('receipt_number')
        payment_type = validated_data.get('payment_type')
        deal_type = validated_data.get('deal_type')
        filter_status = validated_data.get('status') # Renamed to avoid conflict with HTTP status
        agent_name = validated_data.get('agent_name')
        unit_number = validated_data.get('unit_number')
        building_name = validated_data.get('building_name')


       
        try:
            
            current_user_obj = Users.objects.get(email=request.user.email) # Assuming request.user is Django's User model
            user_account_id = current_user_obj.account_id
            print()
            queryset = Receipts.objects.all().order_by('-date')
        except Users.DoesNotExist:
            return Response({"error": "User or account not found."}, status=status.HTTP_404_NOT_FOUND)
        except AttributeError:
            # Handle cases where request.user might not have email or account_id directly
            return Response({"error": "Authentication error or missing user data."}, status=status.HTTP_401_UNAUTHORIZED)


        # --- Apply Global Search Filter ---
        if global_search_value:
            global_q_object = Q() # Start with an empty Q object for global search

            # Add fields to global search based on your specific request
            global_q_object |= Q(receipt_number__icontains=global_search_value)
            global_q_object |= Q(payment_type__icontains=global_search_value)
            global_q_object |= Q(deal_type__icontains=global_search_value)
            global_q_object |= Q(status__icontains=global_search_value) # Using 'status' as field name
            global_q_object |= Q(agent_name__icontains=global_search_value)
            global_q_object |= Q(unit_number__icontains=global_search_value)
            global_q_object |= Q(building_name__icontains=global_search_value)
            try:
                # Attempt to parse the search_term as DD-MM-YYYY
                parsed_date = datetime.strptime(global_search_value, '%d-%m-%Y').date()
                # If successful, format it to YYYY-MM-DD for database comparison
                formatted_date_for_db = parsed_date.strftime('%Y-%m-%d')
                print(formatted_date_for_db)

                # Now add these date filters using the correctly formatted date.
                # For exact date match:
                global_q_object |= Q(date=formatted_date_for_db)
                global_q_object |= Q(sec_date=formatted_date_for_db)
                # combined_q_object |= Q(deal_end_date=formatted_date_for_db)

                # If your date fields are DATETIME/TIMESTAMP, you might need a range query
                # For example, to search for '2017-04-11' in a DATETIME field:
                # from datetime import timedelta
                # end_of_day = parsed_date + timedelta(days=1)
                # combined_q_object |= Q(date__range=(parsed_date, end_of_day))
                # combined_q_object |= Q(deal_start_date__range=(parsed_date, end_of_day))
                # combined_q_object |= Q(deal_end_date__range=(parsed_date, end_of_day))


            except ValueError:
                # If search_term is not a valid DD-MM-YYYY date, then skip adding date filters.
                # This means date fields will not be searched if the input is not a valid date.
                pass

 
 

            queryset = queryset.filter(global_q_object)
 


        # --- Calculate recordsFiltered (after all filters, before pagination) ---
        records_filtered = queryset.count()

    

        # --- Apply Pagination ---
        paginated_queryset = queryset[start:start + length]

        # --- Serialize Data for Response ---
        # Use the ReceiptsSerializer to convert queryset objects to JSON
        serializer = ReceiptSerilizer(paginated_queryset, many=True, context={'request': request})
        print(serializer.data)

        # --- Prepare Response ---
        response_data = {
            "draw": draw,
            "recordsTotal": Receipts.objects.count(), # Total records for the account
            "recordsFiltered": records_filtered, # Records after all filters applied
            "data": serializer.data, # The serialized data for the current page
        }

        return Response(response_data, status=status.HTTP_200_OK)
    

    def create_recicept(self,request):
        receipt_number = request.data.get("receipt_number")
        print(request.data)
        mutable_data  = request.data.copy()

        if Receipts.objects.filter(receipt_number=receipt_number).exists():
            return Response(
                {"error": f"Receipt number {receipt_number} is already taken."},
                status=status.HTTP_400_BAD_REQUEST
            )

        mutable_data['account_id'] = request.user.account_id
        mutable_data['mail_status'] = "sent"


        serializer = ReceiptSerilizer(data=mutable_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


      

    def reciecpt_update(self,request,pk =None):
        reciecpt = get_object_or_404(Receipts, pk=pk)

        if request.method == 'GET':
            serializer = ReceiptSerilizer(reciecpt)
            return Response(serializer.data)

        elif request.method == 'PUT':
            print(request.data)

            
            mutable_data = request.data.copy()

            flat_data = {key: value[0] if isinstance(value, list) else value for key, value in mutable_data.lists()}

            if flat_data['payment_type'] == 'Bank Transfer':
                # chequeNo is not required for Bank Transfer
                print("enter payment")
              

                flat_data['cheque_no'] = ""

            

           
            print("Mutable data = ",mutable_data)
            serializer = ReceiptSerilizer(reciecpt, data= flat_data,partial=True )
            if serializer.is_valid():
                serializer.save()

                print()
                # reciecpt = get_object_or_404(Receipts, pk=pk)

                # serializer = ReceiptSerilizer(reciecpt)
                print(serializer.data)
                return Response(serializer.data)
            return Response(serializer.errors, status=400)


    
         


Receipts_Viewset_filter = Receipts_ViewSet.as_view({'post': 'reciecptstable_filter' }) 
Receipts_Viewset_create = Receipts_ViewSet.as_view({'post': 'create_recicept' }) 
Receipts_ViewSet_update = Receipts_ViewSet.as_view({
    'get': 'reciecpt_update',
    'put': 'reciecpt_update',
})


# serving datatable view html page
def reciept_table_view(request):
    return render(request , "home/recieptslist.html")

# serving the edit recipt html page
def edit_recipt_deal_view(request, pk=None): 
    deal = Receipts.objects.get(pk=pk)
    aws_url = settings.AWS_URL
    # account_id = request.user.account_id
    # try:
    #     agent_group = Group.objects.get(name="Agent")  # Adjust group name if needed
    #     agents = Users.objects.filter(is_active=True)
    # except Group.DoesNotExist:
    #         agents = Users.objects.none()
    
    agents = Users.objects.filter(is_active=True,  account_id = request.user.account_id)
    agents = AgentDropdownSerializer(agents, many=True).data

 
    reciecpt_data = {
        'agents': agents
    }
       

    return render(request, 'home/reciecpt_edit.html', {'receipt_id': pk,    "reciecpt_data" :  json.dumps(reciecpt_data), })

#serving the  create html page
def recicept_create(request):
    latest = Receipts.objects.order_by('-receipt_number').first()
    next_receipt = int(latest.receipt_number) + 1 if latest and latest.receipt_number else 1

    agents = Users.objects.filter(is_active=True,  account_id = request.user.account_id)
    agents = AgentDropdownSerializer(agents, many=True).data
    reciecpt_data = {
        'agents': agents
    }

    return render(request, "home/reciecpt_create.html", {
        "next_receipt_number": next_receipt,"reciecpt_data" :  json.dumps(reciecpt_data)
    })

# serving the reccept_view html page
def recicept_view(request,pk=None):
    reciecpt = get_object_or_404(Receipts, pk=pk)

    serializer = ReceiptSerilizer(reciecpt)
    print(serializer.data)
    return render(request, "home/reciecpt_view.html" ,{'recicept':serializer.data})


# Download the recipt we will convert the html to dowmload the recipt format 
def download_receipt_pdf(request, receipt_id):
    receipt = Receipts.objects.get(id=receipt_id)
    html_string = render_to_string('home/recicepts_pdf.html', {'receipt': receipt})
    html = HTML(string=html_string, base_url=request.build_absolute_uri('/'))
    pdf_file = html.write_pdf()

    download = request.GET.get("download") == "1"
    disposition = 'attachment' if download else 'inline'

    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'{disposition}; filename="receipt_{receipt.receipt_number}.pdf"'
    return response
    
    
