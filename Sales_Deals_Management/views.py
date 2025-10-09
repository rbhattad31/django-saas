import datetime
from linecache import cache
import re
from django.db.models import Subquery, OuterRef
import time
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from rest_framework.response import Response
import json
from django.conf import settings
from Rental_Deal.serializers import ReceiptDropdownSerilizer
from core.models import Receipts, SalesDeals
from core.models import Users 
from django.contrib.auth.models import Group
from rest_framework.decorators import action
from .serializers import SalesDealSerializer, SalesDealSerializerForDraft, SalesDealSerializerFordatafilter , filterSerializer, AgentDropdownSerializer
from django.db.models import Q
from django.template import loader
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse
from .forms import SalesDealsForm 
from django.template import TemplateDoesNotExist
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from Rental_Deal.Utilities import upload_file_to_full_s3_url, delete_from_s3


# Create your views here.
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from rest_framework import viewsets, status, permissions
from rest_framework.permissions import IsAuthenticated

from .serializers import filterSerializer
# from .pagination import CustomPagination  
# from rest_framework.pagination import PageNumberPagination  
from .forms import LoginForm, SignUpForm  # Add this import for LoginForm and SignUpForm
   

from django.template import loader
from django import template
from django.urls import reverse
from django.utils.timezone import now



from django.db.models import Q



class SalesDealViewSet(viewsets.ModelViewSet):
    # queryset = SalesDeals.objects.all()
    serializer_class = SalesDealSerializer
    permission_classes = [IsAuthenticated]
    

    @action(detail=True, methods=['delete'], url_path='delete')
    def delete_sales(self, request, pk=None):
        sales = get_object_or_404(SalesDeals, pk=pk)
        sales.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


    @action(detail=True, methods=['get'], url_path='view')
    def view_sales_deal(self, request, pk=None):
        sales_deal = get_object_or_404(SalesDeals, pk=pk)
        print("Sales Deal:", sales_deal)
        serializer = SalesDealSerializer(sales_deal,context ={'request': request})
        # return HttpResponse("hello this is view page")
        aws_url = settings.AWS_URL+"sale/referencenumber_CPS/"

        # receipt_no = Receipts.objects.filter(id =sales_deal.receipt_no).first()
        # if not sales_deal.receipt_no:
        #     recipt_no = None
        # else:
        #     recipt_no = Receipts.objects.filter(id=sales_deal.receipt_no).first() 
        #     print(recipt_no.receipt_number , "this is recipt id ")

        if sales_deal.receipt_no == "Null" or sales_deal.receipt_no == "":
        # Case 1: Explicit "Null" → no receipt
            recipt_no = "Null"
            recipt_id = ""
            
         

        elif sales_deal.receipt_no == "No Commission":
            # Case 2: No Commission special case
            recipt_no = "No Comission"
            recipt_id = ""
            

        

        else:
            # Case 3: Receipt ID
            recipt = Receipts.objects.filter(id=sales_deal.receipt_no).first()
            if recipt:
                recipt_no = recipt.receipt_number
                recipt_id = recipt.id
                print(recipt_no , "this is recipt number ")
                print(recipt_id , "this is recipt id ")
            else:
                recipt_no = ""
                recipt_id = ""

        return render(request, 'home/viewsalesdeal.html', {'salesdeal': serializer.data, 'aws_base_url': aws_url, "receipt_no": recipt_no, "receipt_id": recipt_id})


    @action(detail=False, methods=['post'], url_path='create-sale-deal')
    def create_sale_deal(self, request):
        if not request.user.has_perm("core.add_salesdeals"):
            return Response({"detail": "You do not have permission to access this."}, status=status.HTTP_403_FORBIDDEN)


        updated_files = {}
        base_field_name = ""
        removed_clean_dict = {}
        print(request.data)
        mutable_data = request.data.dict().copy()
        print(request.user)
        print(request.user.id)
        print(mutable_data)

                # userobj = Users.objects.filter(pk = request.user.id)

        print(f"DEBUG: save_as received: {mutable_data.get('save_as')}") # <--- ADD THIS
        if mutable_data.get('save_as') == "create-deal":
            mutable_data['form_status'] = "Complete"
        else:
            mutable_data['form_status'] = "Incomplete"
        print(f"DEBUG: form_status set to: {mutable_data['form_status']}") # <--- ADD THIS
        print(f"DEBUG: mutable_data before serializer: {mutable_data}") 



        
        # adding reference number to the table of recipts 
        try:
            receipt_id = mutable_data.get("receipt_no")
            if receipt_id.isdigit():
                Receipts.objects.filter(id=receipt_id).update(deal_refer_no=mutable_data['reference_number'])
                Receipts.objects.filter(id=mutable_data['receipt_no']).update(status="Used")
                print(f"Updated receipt_no {receipt_id} with reference_number {mutable_data['reference_number']}")

            else:
                pass
        except (ValueError, TypeError):
            print("Invalid receipt_no or not provided, skipping update.")
        
        print(mutable_data)

        mutable_data['submitted_by_user'] = request.user.id
        mutable_data['account'] = request.user.account_id
        mutable_data['created_by'] = request.user.id
        mutable_data['submitted_by_agent'] = request.user.id
       
           


        # if 'submitted_date' in mutable_data and mutable_data['submitted_date']:
        #     dmy_date = mutable_data['submitted_date']  # e.g. "01-08-2025"
        #     day, month, year = dmy_date.split("-")
        #     ymd_date = f"{year}-{month}-{day}" 
            
        #     mutable_data['submitted_date'] = ymd_date  # becomes "2025-08-01"

        # mutable_data['date'] = mutable_data.get("submitted_date") or timezone.now().date()

       


        #  check for the  non fiel field  if they are valid then update the serializer 
        print(f"multable data  acoount_id {mutable_data['account']}")
        if mutable_data['form_status']  == "Complete":
            mutable_data['submitted_date']= datetime.date.today() #changes htes data  to teh submitted date in the froet end
             
            serializer = self.get_serializer(data=mutable_data, partial=True)
        else:
            serializer = SalesDealSerializerForDraft(data=mutable_data ,partial=True)

        serializer.is_valid(raise_exception=True)
       



        # sales_deal = get_object_or_404(RentalDeals, pk=pk)
        path = f"sales/referencenumber_CP/{mutable_data['reference_number']}"
        for key in request.FILES.keys():
            base_field_name = key.rstrip("[]")  # Remove [] suffix if present
            print("base_field_name", base_field_name)
            files = request.FILES.getlist(key)

        

            # Get existing value from the DB field (comma-separated filenames)
            # existing_value = getattr(sales_deal, base_field_name, "")
            # existing_files = existing_value.split(",") if existing_value else []

            
            for file in files:
                timestamp = int(time.time())
                cleaned_name = re.sub(r"[,]+", " ", file.name)
                filename = f"{base_field_name}{timestamp} {cleaned_name}"
                filepath = f"{path}/{filename}"

                # is_uploaded = upload_file_to_full_s3_url(file, filepath)

                # if is_uploaded:
                    # new_file_names.append(filename)


                if base_field_name not in updated_files:
                    updated_files[base_field_name] = []
                updated_files[base_field_name].append(filename)

                print("updated_files", updated_files)
            
        final_updated_values = {}

        all_field_keys = set(updated_files.keys()) | set(removed_clean_dict.keys())

        for base_field_name in all_field_keys:
            reference_number = mutable_data.get("reference_number")
            path_folder = f"sales/referencenumber_CP/{reference_number}"

       

            # ✅ Add new files
            new_file_names = []
            for file in request.FILES.getlist(base_field_name + "[]"):
                timestamp = int(time.time())
                cleaned_name = re.sub(r"[,]+", " ", file.name)
                filename = f"{base_field_name}{timestamp} {cleaned_name}"
                relative_path = f"{path_folder}/{filename}"

                is_uploaded = upload_file_to_full_s3_url(file, relative_path)
                if is_uploaded:
                    new_file_names.append(filename)

            # ✅ Combine and update mutable_data + DB dict
            combined_files =   new_file_names
            combined_str = ",".join(combined_files)

            # mutable_data[base_field_name] = combined_str
            final_updated_values[base_field_name] = combined_str



        for base_field_name, combined_str in final_updated_values.items():
            mutable_data[base_field_name] = combined_str 
            print(f"Updated mutable_data[{base_field_name}]:", mutable_data[base_field_name])

            
        mutable_data['created_by'] = request.user.email
        mutable_data['created_at'] = now()

        

        

        if mutable_data['form_status']  == "Complete":

            serializer = self.get_serializer(data=mutable_data)
        else:
            serializer = SalesDealSerializerForDraft(data=mutable_data )

        serializer.is_valid(raise_exception=True)

        
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


    
    @action(detail=False, methods=['get','put'], url_path='update')
    def update_sales_deal(self, request,pk=None):
        if not request.user.has_perm("core.change_salesdeals"):
            return Response({"detail": "You do not have permission to access this."}, status=status.HTTP_403_FORBIDDEN)

        if request.method == 'GET':
            pk = pk
            sales_deal = get_object_or_404(SalesDeals, pk=pk)
            serializer = SalesDealSerializer(sales_deal,   partial=True ,context ={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
            
            # return render(request, 'home/editsalesdeal.html', {'salesdeal': serializer.data})
        elif request.method == 'PUT':
            print("request data", request.data)
            print("✅ Files:", request.FILES) 
            # print("Keys in request.data:", request.data.keys())
            print("Files:", request.FILES.keys())
            sales_deal = get_object_or_404(SalesDeals, pk=pk)
            declared_file_fields = request.POST.get('__file_fields__', '').split(',')
            print("Declared file fields:", declared_file_fields)

            print("sales_deal", sales_deal)

            #
            removed_fields = {
                key[:-8]: value.strip()
                for key, value in request.POST.items()
                if key.endswith('_removed') and value.strip()
}
            print("Removed fields:", removed_fields)

            mutable_data = request.data.dict().copy()
            file_name_to_remove_list = []
            existing_files = []
            new_file_names = []
            updated_files = {}
            base_field_name = ""
            removed_clean_dict = {}


            for base_field_name in removed_fields:
                existing_value_from_db = getattr(sales_deal, base_field_name, "")
                print("existing_value_from_db", existing_value_from_db )
                existing_files_names_from_db = existing_value_from_db.split(",") if existing_value_from_db else []
                print("existing_files_names_from_db", existing_files_names_from_db)
                removed_clean_list = [f.strip() for f in removed_fields[base_field_name].split(",")]
                print("removed_clean_list", removed_clean_list)
                removed_clean_dict = {
                key: [f.strip() for f in value.split(",") if f.strip()]
                    for key, value in removed_fields.items()
                }
                print()
                print("removed_clean_dict", removed_clean_dict)

                for file_name in existing_files_names_from_db:
                    file_name_clean = file_name.strip()
                    
                    
                    print("file_name repr:", repr(file_name_clean))
                    print("removed_list repr:", [repr(f) for f in removed_clean_list])
                    print("file_name", file_name)
                    value = file_name in removed_clean_list
                    print("Checking if file_name is in removed_fields:", file_name, "in", removed_fields[base_field_name])
                    print("value", value)
                    if value:
                        # Remove the file from S3
                        filepath = f"sale/referencenumber_CPS/{sales_deal.reference_number}/{file_name}"

                        # is_deleted= delete_from_s3(filepath)
                        # print( "filepath", filepath)
                        # print("is_deleted", is_deleted)

                        # if is_deleted:
                            # existing_files_names_from_db.remove(file_name)
                        print(f"✅ Deleted from S3: file {file_name} at  ")
                        print("after removing file_names", existing_files_names_from_db)
                        print()
                        print(file_name)

                        file_name_to_remove_list.append(file_name)

                        print("file_name_to_remove_list", file_name_to_remove_list)


                        

    # Loop through all uploaded file fields
    # add data 
            path = f"sale/referencenumber_CPS/{mutable_data['reference_number']}"
            for key in request.FILES.keys():
                base_field_name = key.rstrip("[]")  # Remove [] suffix if present
                print("base_field_name", base_field_name)
                files = request.FILES.getlist(key)
 
            

                # Get existing value from the DB field (comma-separated filenames)
                # existing_value = getattr(sales_deal, base_field_name, "")
                # existing_files = existing_value.split(",") if existing_value else []

                
                for file in files:
                    timestamp = int(time.time())
                    cleaned_name = re.sub(r"[,]+", " ", file.name)
                    filename = f"{base_field_name}{timestamp} {cleaned_name}"
                    filepath = f"{path}/{filename}"

                    # is_uploaded = upload_file_to_full_s3_url(file, filepath)

                    # if is_uploaded:
                        # new_file_names.append(filename)


                    if base_field_name not in updated_files:
                        updated_files[base_field_name] = []
                    updated_files[base_field_name].append(filename)

                    print("updated_files", updated_files)
                    
                # Merge old and new file names
            for file_name_to_remove in file_name_to_remove_list:
                if file_name_to_remove in existing_files:
                    existing_files.remove(file_name_to_remove)

            combined_files = existing_files + new_file_names

            combined_str = ",".join(filter(None, combined_files))
            print("combined_str", combined_str)

            common_keys = list(set(removed_clean_dict.keys()) & set(updated_files.keys()))

            print("✅ common_keys", common_keys)


                # Set updated string into request.data copy
            # mutable_data[base_field_name] = combined_str

             
            # // new code 
            final_updated_values = {}

            all_field_keys = set(updated_files.keys()) | set(removed_clean_dict.keys())

            for base_field_name in all_field_keys:
                reference_number = mutable_data.get("reference_number")
                path_folder = f"sale/referencenumber_CPS/{reference_number}"

                existing_value = getattr(sales_deal, base_field_name, "")
                existing_files = existing_value.split(",") if existing_value else []

                updated_existing_files = []

                # ✅ Remove files if present in removed_clean_dict
                files_to_remove = removed_clean_dict.get(base_field_name, [])
                for file_name in existing_files:
                    file_name = file_name.strip()
                    if file_name in files_to_remove:
                        relative_path = f"{path_folder}/{file_name}"
                        is_deleted = delete_from_s3(relative_path)
                        if not is_deleted:
                            updated_existing_files.append(file_name)  # keep if deletion failed
                    else:
                        updated_existing_files.append(file_name)

                # ✅ Add new files
                new_file_names = []
                for file in request.FILES.getlist(base_field_name + "[]"):
                    timestamp = int(time.time())
                    cleaned_name = re.sub(r"[,]+", " ", file.name)
                    filename = f"{base_field_name}{timestamp} {cleaned_name}"
                    relative_path = f"{path_folder}/{filename}"

                    is_uploaded = upload_file_to_full_s3_url(file, relative_path)
                    if is_uploaded:
                        new_file_names.append(filename)

                # ✅ Combine and update mutable_data + DB dict
                combined_files = updated_existing_files + new_file_names
                combined_str = ",".join(combined_files)

                # mutable_data[base_field_name] = combined_str
                final_updated_values[base_field_name] = combined_str



            for base_field_name, combined_str in final_updated_values.items():
                mutable_data[base_field_name] = combined_str 
                print(f"Updated mutable_data[{base_field_name}]:", mutable_data[base_field_name])


            

            if mutable_data.get('save_as') == "update-deal":
                mutable_data['form_status'] = "Complete"
                is_submitted_date = getattr(sales_deal, 'submitted_date' , "")
                if not is_submitted_date:
                    mutable_data['submitted_date']= datetime.date.today()
            else:
                mutable_data['form_status'] = "Incomplete"
            print(f"DEBUG: form_status set to: {mutable_data['form_status']}")


            if mutable_data.get("is_approved_rejected") and mutable_data.get("is_approved_rejected") in ["A", "R", "F"]:
                mutable_data['approved_rejected_by'] = request.user.email
            
            if mutable_data.get('receipt_no'):
                if mutable_data['receipt_no'].isdigit():
                    print("this is the receipt no", mutable_data['receipt_no'])
                    Receipts.objects.filter(id=mutable_data['receipt_no']).update(deal_refer_no=mutable_data['reference_number'])
                    Receipts.objects.filter(id=mutable_data['receipt_no']).update(status="Used")
                else:
                    pass


 
            mutable_data['updated_by'] = request.user.email
            mutable_data['updated_at'] = now()

            
            
                 
                       

            print("mutable_data", mutable_data)
            # Now pass this updated data to serializer
            serializer = self.get_serializer(sales_deal, data=mutable_data, partial=True)

            # serializer = self.get_serializer(sales_deal, data=request.data, partial=True)

                # ✅ Update data from form
                # serializer = self.get_serializer(sales_deal, data=request.data, partial=True)
                
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data ,status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
 
    @action(detail=False, methods=['post'], url_path='filter')
    def datatable_filter(self, request):
        data = filterSerializer(data=request.data)
        data.is_valid(raise_exception=True)
        validated = data.validated_data
        print("Validated Data:", validated) 
        print(request.data)
        print(request.data.get("order") ,"togetordering")
        user = request.user
        print(request.user)
        account_id = user.account_id
        print( "account_from_request",request.user.account_id)

        queryset = (
    SalesDeals.objects 
    .filter(is_deleted="N", account_id=account_id)
    .select_related("submitted_by_user")   # <— prevents N+1 queries
    .order_by("-date").only("id","reference_number", "unit_details", "builduing_name",   "is_approved_rejected","project_name", "seller_name",
    "seller_source","buyer_name","buyer_source","buyer_mobile",
    "selller_mobile","project_name",  "date", "submitted_date", "buyer_name","deal_amount",
   "submitted_by_user","form_status","manager_approved_rejected","account_id","is_deleted",
   "submitted_by_user__id",
        "submitted_by_user__name", "submitted_by_user__email"  
         )
)
        user = Users.objects.annotate(
    first_group_name=Subquery(
        Group.objects.filter(custom_user_set=OuterRef("pk"))
        .order_by("id")  # ensures consistent first group
        .values("name")[:1]  # take only the first group's name
    )
).get(id=request.user.id)
        

        # Global search
        search_term = validated.get("search", {}).get("value") or ''
        if search_term:
            queryset = queryset.filter(
                # Q(email__icontains=search_term) |
                Q(reference_number__icontains=search_term) |
                Q(date__icontains=search_term) |
                Q(unit_details__icontains=search_term) |
                Q(builduing_name__icontains=search_term) |
                Q(project_name__icontains=search_term) |
                Q(unit_details__icontains=search_term) |

                Q(deal_amount__icontains=search_term) |
                Q(submitted_date__icontains=search_term)
            )
            print("Search Term:", search_term)  # Debugging line
        # Debugging line
        # Field-specific filters
        filter_fields = [
            "reference_number", "unit_details", "building_name","seller_source","selller_mobile"
            "is_approved_rejected", "project_name","seller_name","buyer_name","buyer_mobile","buyer_source",
           ]
        for field in filter_fields:
            value = validated.get(field)
            if value:
                filter_kwargs = {f"{field}__icontains": value}
                queryset = queryset.filter(**filter_kwargs)

        # Deal Type Filter
        type_filter = validated.get("type")
        print("type_filter", type_filter)

        user_role = user.first_group_name or ""
        role = user_role.split("-", 1)[1] if "-" in user_role else user_role
        print(user_role)
        print(role)
        if type_filter:
    # ---------------- Pending ----------------
            if type_filter == "pending":
                if user.has_perm("core.view_pending_sales_deals"):
                    if account_id and (role in ["Manager","Agent"] or user.is_superuser):
                        queryset = queryset.filter(manager_approved_rejected="P", form_status="Complete")
                    else:
                        queryset = queryset.filter(is_approved_rejected="P", manager_approved_rejected="A", form_status="Complete")
                else:
                    return Response({"detail": "You do not have permission: view_pending_sales_deals"}, status=status.HTTP_403_FORBIDDEN)

            # ---------------- Approved ----------------
            elif type_filter == "approved":
                if user.has_perm("core.view_approved_sales_deals"):
                    if account_id and (role in ["Manager", "Agent"] or user.is_superuser):
                        queryset = queryset.filter(manager_approved_rejected="A", form_status="Complete")
                    else:
                        queryset = queryset.filter(is_approved_rejected="A", form_status="Complete")
                else:
                    return Response({"detail": "You do not have permission: view_approved_sales_deals"}, status=status.HTTP_403_FORBIDDEN)

            # ---------------- Rejected ----------------
            elif type_filter == "rejected":
                if user.has_perm("core.view_rejected_sales_deals"):
                    if account_id and (role in ["Manager", "Agent"] or user.is_superuser):
                        queryset = queryset.filter(manager_approved_rejected="R", form_status="Complete")
                    else:
                        queryset = queryset.filter(is_approved_rejected="R", form_status="Complete")
                else:
                    return Response({"detail": "You do not have permission: view_rejected_sales_deals"}, status=status.HTTP_403_FORBIDDEN)

            # ---------------- Waiting Finance ----------------
            elif type_filter == "waiting":
                if user.has_perm("core.view_waiting_finance_sales_deals"):
                    queryset = queryset.filter(is_approved_rejected="F")
                else:
                    return Response({"detail": "You do not have permission: view_waiting_finance_sales_deals"}, status=status.HTTP_403_FORBIDDEN)

            # ---------------- Entered Finance ----------------
            elif type_filter == "entered-finance":
                if user.has_perm("core.enter_finance_sales_deal"):
                    queryset = queryset.filter(is_entered_in_finance_system="1", form_status="Complete")
                else:
                    return Response({"detail": "You do not have permission: enter_finance_sales_deal"}, status=status.HTTP_403_FORBIDDEN)

            # ---------------- Pending Finance ----------------
            elif type_filter == "pending-finance":
                if user.has_perm("core.view_pending_finance_sales_deal"):
                    queryset = queryset.filter(is_entered_in_finance_system="0", form_status="Complete")
                else:
                    return Response({"detail": "You do not have permission: view_pending_finance_sales_deal"}, status=status.HTTP_403_FORBIDDEN)

            # ---------------- Draft ----------------
            elif type_filter == "draft":
                if user.has_perm("core.view_my_draft_sales_deals"):
                    queryset = queryset.filter(form_status="Incomplete")
                else:
                    return Response({"detail": "You do not have permission: view_my_draft_sales_deals"}, status=status.HTTP_403_FORBIDDEN)

            # ---------------- All ----------------
            elif type_filter == "All":
                if user.has_perm("core.view_all_sales_deals"):
                    queryset = queryset.filter(form_status="Complete")
                else:
                    return Response({"detail": "You do not have permission: view_all_sales_deals"}, status=status.HTTP_403_FORBIDDEN)


            if role == "Agent" or user_role == "Agent":
                queryset = queryset.filter(submitted_by_user=user)
            elif (role == "Admin" or user_role == "Admin") and type_filter == "draft":
                queryset = queryset.filter(created_by=user.email)
            else:
                role = "superadmin"

        # Date range filter

        if validated.get("from_date"):
            queryset = queryset.filter(date__gte=validated.get("from_date"))
        if validated.get("to_date"):
            queryset = queryset.filter(date__lte=validated.get("to_date"))

        total_count = queryset.count()

        # Manual Pagination for DataTables
        start = validated.get("start", 0)
        length = validated.get("length", 10)
        paginated = queryset[start:start + length]
        

        serializer = SalesDealSerializerFordatafilter(paginated, many=True,context= {'request': request})
        response_data = {
            "draw": validated.get("draw", 0),
            "recordsTotal": total_count,
            "recordsFiltered": total_count,
            "data": serializer.data,
        }
        return Response(response_data)
    





    def update_single_field(self, request):
        if request.method == 'PUT':
            try:
                print("Request data for single field update:", request.body)
                data =  request.data
                obj_id = data.get('object_id')
                field_name = data.get('field_name')
                value = data.get('value')
                print("Data received for update:", data)

                # Make sure field is valid
                if field_name not in [f.name for f in SalesDeals._meta.get_fields()]:
                    print("inside the ifcconditionof sale deaks ")
                    return Response({'status': 'error', 'message': 'Invalid field name'}, status=400)

# Update directly in DB
                SalesDeals.objects.filter(id=obj_id).update(**{field_name: value})

                updated_deal = SalesDeals.objects.get(id=obj_id)

                return Response({'status': 'success',"updated_value":  getattr(updated_deal, field_name) })

            except Exception as e:
                return Response({'status': 'error', 'message': str(e)}, status=400)

        return Response({'status': 'error', 'message': 'Invalid request'}, status=400)


SalesDealViewSet_filter = SalesDealViewSet.as_view({'post': 'datatable_filter'})
SalesDealViewSet_update = SalesDealViewSet.as_view({'put': 'update_sales_deal', 'get': 'update_sales_deal'})
Sales_DealViewSet_update_single_field = SalesDealViewSet.as_view({'put': 'update_single_field'})
SalesDealViewSet_create = SalesDealViewSet.as_view({'post': 'create_sale_deal'})




 
@login_required(login_url="/login/")
@permission_required("core.manage_sales_deals",raise_exception=True)
def all_sales_deals(request):
    """
    View to list all rental deals.
    """
    return render(request, 'home/Salesall.html')


 # Ensure this form exists

# @login_required

from django.http import JsonResponse
from django.urls import reverse

from django.utils import timezone

@login_required(login_url="/login/")
@permission_required("core.add_salesdeals",raise_exception=True)
def create_sales_deal_page(request):
   
    agents=Users.objects.filter(is_active=True,account_id=request.user.account_id)
    agents=AgentDropdownSerializer(agents,many=True).data

    group = request.user.groups.first().name
    print(group)
    role = group.split("-", 1)[1] if "-" in group else group
    # user_role = request.user.first_group_name or ""
    # role = user_role.split("-", 1)[1] if "-" in user_role else user_role

    print(role)

    reciepts_db = Receipts.objects.filter(account_id=request.user.account_id, status="Unused" , agent_id = request.user.id)
    receipts = ReceiptDropdownSerilizer(reciepts_db,many=True).data
    sales_data={
               'agents': agents,
                'receipts': receipts
           }
    print("Agents Data:", agents)
     

    return render(request, 'home/createsalesdeal.html', {'sales_data' : json.dumps(sales_data)})




# render html page of Edit Sale Deal 

@login_required(login_url="/login/")
@permission_required("core.change_salesdeals",raise_exception=True)
def edit_sales_deal_page(request, pk):
    sales_deal = get_object_or_404(SalesDeals, pk=pk)
    aws_url = settings.AWS_URL+"sale/referencenumber_CPS/"
    print("AWS URL:", aws_url)
    # serializer = SalesDealSerializer(sales_deal, partial=True)
    agents = Users.objects.filter(is_active=True ,account_id=request.user.account_id)
    agents = AgentDropdownSerializer(agents, many=True).data


    group = request.user.groups.first().name
    print(group)
    role = group.split("-", 1)[1] if "-" in group else group
    # user_role = request.user.first_group_name or ""
    # role = user_role.split("-", 1)[1] if "-" in user_role else user_role

    print(role)



    if role == "Agent":
        reciepts_db = Receipts.objects.filter(account_id = request.user.account_id , agent_id = request.user.id)
    else:
        reciepts_db = Receipts.objects.filter(account_id = request.user.account_id)

    
    receipts = ReceiptDropdownSerilizer(reciepts_db,many=True).data

    sales_data = {
        'agents': agents,
        'receipts': receipts
    }

    return render(request, 'home/editsalesdeal.html', {'deal_id': pk, 'aws_url': aws_url, 'reference_number': sales_deal.reference_number ,'sales_data': json.dumps(sales_data)})



























