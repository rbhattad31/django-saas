 
from fileinput import filename
import logging
from django.db.models import Subquery, OuterRef, Q, Prefetch
from urllib import request
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
import re
from .Utilities import delete_from_s3, upload_file_to_full_s3_url, s3_file_exists


# Create your views here.
from django.contrib.auth import authenticate, login

from django.contrib.auth.decorators import permission_required
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from core.models import Users
from .forms import RentalDealForm, FinanceCommentForm

from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.decorators import action
from rest_framework.response import Response
from core.models import RentalDeals,Users,Account,Receipts
from .serializers import DealSerializer, filterSerializer, AgentDropdownSerializer, ReceiptDropdownSerilizer,DealSerializerfordatatable
from .pagination import CustomPagination  
from rest_framework.pagination import PageNumberPagination  
# from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .forms import LoginForm, SignUpForm  # Add this import for LoginForm and SignUpForm
from datetime import datetime
from datetime import date
from weasyprint import HTML
from django.template.loader import render_to_string

   

# from django_filters import rest_framework as filters
from django.template import loader
from django import template
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import Group  # Add this import
from django.core.exceptions import PermissionDenied  # <-- Add this import
import os
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.utils.timezone import now # Add this import
import time
import json
# from core.utils import has_cached_permission


from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from django.db.models import Q
from rest_framework.permissions import BasePermission
from rest_framework import status


logger = logging.getLogger('Rental_Deal')


class RentalDealPermissions(BasePermission):
    def has_permission(self, request, view):
        # Map methods to permissions
        perms_map = {
            'GET': 'core.view_rentaldeals',
            'OPTIONS': 'core.view_rentaldeals',
            'HEAD': 'core.view_rentaldeals',
            'POST': 'core.add_rentaldeals',
            'PUT': 'core.change_rentaldeals',
            'PATCH': 'core.change_rentaldeals',
            'DELETE': 'core.delete_rentaldeals',
        }

        required_perm = perms_map.get(request.method)
        if required_perm:
            return request.user.has_perm(required_perm)

        return False


 




class Rental_DealViewSet(viewsets.ModelViewSet):
    queryset = RentalDeals.objects.all()
       # for default `list`, `retrieve`
    pagination_class = CustomPagination 
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Optimized: join submitted_by_user in one query
        return RentalDeals.objects.with_user().all()
   
    
    def get_serializer_class(self):
        if self.action == 'datatable_filter':
            return filterSerializer
        return DealSerializer # Custom pagination class
    # filter bsed on input 
    
    @action(detail=False, methods=['post'] ,url_path='filter')
    def datatable_filter(self, request):
        # print(request.data)
        # print(request.data.get("order") ,"togetordering")
        # user = Users.objects.get(email = request.user)
        user = request.user

        # print(request.user)
        account_id = user.account_id
        # print( "account_from_request",request.user.account_id)
        
       

        queryset = (
    RentalDeals.objects.select_related("submitted_by_user")
    .filter(is_deleted="N", account_id=account_id)
    .order_by("-id")
    .only(
        # === Core fields ===
        "id",
        "submitted_date",
        "submitted_by_user",
        "reference_number",
        "date",
        "unit_details",
        "building_name",
        "project_name",
        "is_new_deal",
        "owner_title",
        "owner_first_name",
        "owner_last_name",
        "owner_source",
        "owner_mobile",
        "owner_email",
        "tenant_title",
        "tenant_first_name",
        "tenant_last_name",
        "tenant_source",
        "tenant_mobile",
        "tenant_email",
        "owner_agency",
        "agent_first_name",
        "agent_last_name",
        "agent_phone",
        "agent_email",
        "brn",
        "tenant_agency",
        "tenant_agent_first_name",
        "tenant_agent_last_name",
        "tenant_agent_phone",
        "tenant_agent_email",
        "tenant_brn",
        "tenancy_contract",
        "owner_passport_copy",
        "tenant_passport_visa_copy",
        "tenant_emirates_id",
        "rental_deposit_cheque_copy",
        "title_deed",
        "owner_poa_pp_copy",
        "key_hand_over_form",
        "total_commission",
        "less_outsude_commission",
        "net_commission",
        "classic",
        "agent1",
        "agent2",
        "agent3",
        "is_approved_rejected",
        "approved_rejected_by",
        "is_entered_in_finance_system",
        "comments",
        "rental_price",
        "ejari",
        "agent_name1",
        "agent_name2",
        "agent_name3",
        "owner_eid_copy",
        "agent_comment",
        "mediating_agency",
        "mediating_agent_name",
        "mediating_agent_phone",
        "mediating_agent_email",
        "mediating_agency_brn",
        "poa_copy",
        "deal_start_date",
        "deal_end_date",
        "receipt_no",
        "form_status",
        "rental_kyc_number",
        "is_rental_aml",
        "kyc_number",
        "comments_finance",
        "created_at",
        "updated_at",
        "created_by",
        "updated_by",
        "account",
        "property",
        "is_deleted",
        "plot_no",
        "mode_of_payment",
        "deal_agent",
        "receipt_id",
        "property_usage",
        "property_size",
        "premises_no",
        "security_deposit",
        "submitted_by_agent",
        "property_type",
        "tenancy_application_form",
        "screening",
        "screening_comments",
        "seller_nationality",
        "buyer_nationality",
        "manager_approved_rejected",
        # === Related user fields ===
        "submitted_by_user__id",
        "submitted_by_user__name",
        "submitted_by_user__email",
    )
)
 # Filter out deleted deals
        # print("Initial queryset count:", queryset)

        user = Users.objects.annotate(
    first_group_name=Subquery(
        Group.objects.filter(custom_user_set=OuterRef("pk"))
        .order_by("id")  # ensures consistent first group
        .values("name")[:1]  # take only the first group's name
    )
        ).get(id=request.user.id)

         
       
         
        # user = Users.objects.get(email = request.user)
      
        

        
        # print("Request data:", request.data)
        data = filterSerializer(data=request.data)
        data.is_valid(raise_exception=True)
        print()
        data = data.validated_data
        # print("validated", data)


       

        






        # Global search
        search_term = data.get("search", {}).get("value") or ''
        print(search_term , "point x1")
        if search_term:
            normalized_search_replace_slash = search_term.replace("/", "-")
            normalized_search_replace_minus = search_term.replace("-", "/")
            combined_q_object = Q()

            # combined_q_object |= Q(reference_number__icontains=normalized_search)
            combined_q_object |= Q(submitted_by_user__name__icontains=search_term)
            combined_q_object |= (Q(reference_number__icontains=search_term)|Q(reference_number__icontains=normalized_search_replace_slash) |
    Q(reference_number__icontains=normalized_search_replace_minus) )
            
            combined_q_object |= Q(unit_details__icontains=search_term)
            combined_q_object |= Q(building_name__icontains=search_term)
            combined_q_object |= Q(project_name__icontains=search_term)
            combined_q_object |= Q(owner_first_name__icontains=search_term)
            combined_q_object |= Q(owner_last_name__icontains=search_term)
            combined_q_object |= Q(owner_mobile__icontains=search_term)
            combined_q_object |= Q(owner_email__icontains=search_term)
            combined_q_object |= Q(tenant_first_name__icontains=search_term)
            combined_q_object |= Q(tenant_last_name__icontains=search_term)
            combined_q_object |= Q(tenant_mobile__icontains=search_term)
            combined_q_object |= Q(tenant_email__icontains=search_term)

            # --- Specific Handling for Date Fields ---
            try:
                # Attempt to parse the search_term as DD-MM-YYYY
                parsed_date = datetime.strptime(search_term, '%d-%m-%Y').date()
                # If successful, format it to YYYY-MM-DD for database comparison
                formatted_date_for_db = parsed_date.strftime('%Y-%m-%d')
               

                # Now add these date filters using the correctly formatted date.
                # For exact date match:
                combined_q_object |= Q(date=formatted_date_for_db)
                combined_q_object |= Q(deal_start_date=formatted_date_for_db)
                combined_q_object |= Q(deal_end_date=formatted_date_for_db)

                


            except ValueError:
                # If search_term is not a valid DD-MM-YYYY date, then skip adding date filters.
                # This means date fields will not be searched if the input is not a valid date.
                pass

            # Apply the combined Q object to the queryset
            # print("point x2", queryset)
            queryset = queryset.filter(combined_q_object)

        # Field-specific filters
        filter_fields = [
            "reference_number", "unit_details", "building_name", "is_new_deal",
            "is_approved_rejected", "project_name", "owner_first_name", "tenant_first_name",
            "owner_mobile", "tenant_mobile"
        ]
        print(data)
        print(filter_fields , "point x3")
        for field in filter_fields:
          
            value = data.get(field)
            print(filter_fields , "point x4")
            if value:
                print(f"Filtering {field} by {value}")
                print(filter_fields , "point x5")
                
                queryset = queryset.filter(**{f"{field}__icontains": value})

        # Filterationon types keyword
        type_filter = data.get("type")
        print(type_filter)
        user_role = user.first_group_name or ""
        role = user_role.split("-", 1)[1] if "-" in user_role else user_role
        # print(user_role)
        # print(role)
        print(queryset)
 

        if type_filter:
            # ---------------- Pending ----------------
            if type_filter == "pending":
                if user.has_perm("core.view_pending_rental_deals"):
                    if account_id and (role in ["Manager","Agent"] or user.is_superuser):
                        queryset = queryset.filter(manager_approved_rejected="P", form_status="Complete")
                    else:
                        print( "entere the admin pending")
                        print(len(queryset))
                        queryset = queryset.filter(is_approved_rejected="P", manager_approved_rejected="A", form_status="Complete")
                        print(len(queryset))
                else:
                     return Response(
    {"detail": "You do not have permission to access this."},
    status=status.HTTP_403_FORBIDDEN
                )  # 🚨 Forbidden

            # ---------------- Approved ----------------
            elif type_filter == "approved":
                if user.has_perm("core.view_approved_rental_deals"):
                    if account_id and (role in ["Manager"] or user.is_superuser):
                        queryset = queryset.filter(manager_approved_rejected="A", form_status="Complete")
                    elif role not in ["Agent"]:
                        queryset = queryset.filter(is_approved_rejected="A", form_status="Complete")
                else:
                     return Response({"detail": "You do not have permission to access this."},
    status=status.HTTP_403_FORBIDDEN)

            # ---------------- Rejected ----------------
            elif type_filter == "rejected":
                if user.has_perm("core.view_rejected_rental_deals"):
                    if account_id and (role in ["Manager"] or user.is_superuser):
                        queryset = queryset.filter(Q(manager_approved_rejected="R", form_status="Complete")) 
                    elif role not in ["Agent"]:
                        print("enter the admin rejected block finace")
                        queryset = queryset.filter(is_approved_rejected="R", form_status="Complete")
                        print(queryset)
                else:
                     return Response(
    {"detail": "You do not have permission to access this."},
    status=status.HTTP_403_FORBIDDEN
)

            # ---------------- Waiting Finance ----------------
            elif type_filter == "waiting-finance":
                if user.has_perm("core.view_waiting_finance_rental_deals"):
                    queryset = queryset.filter(is_approved_rejected="F")
                else:
                    return Response({"detail": "You do not have permission to access this."}, status=status.HTTP_403_FORBIDDEN)
            # ---------------- Entered Finance ----------------
            elif type_filter == "entered-finance":
                if user.has_perm("core.enter_finance_rental_deals"):
                    queryset = queryset.filter(is_entered_in_finance_system="1", form_status="Complete").filter(
            is_approved_rejected__in=["F", "A"]
            )
                else:
                     return Response(
    {"detail": "You do not have permission to access this."},
    status=status.HTTP_403_FORBIDDEN
)

            # ---------------- Pending Finance ----------------
            elif type_filter == "pending-finance":
                if user.has_perm("core.view_pending_finance_rental_deals"):
                    queryset = queryset.filter(is_entered_in_finance_system="0", form_status="Complete").filter(
                    is_approved_rejected__in=["F", "A"]
                        )
                else:
                     return Response(
                        {"detail": "You do not have permission to access this."},
                        status=status.HTTP_403_FORBIDDEN
                    )

            # ---------------- Draft ----------------
            elif type_filter == "draft":
                if user.has_perm("core.view_my_draft_rental_deals"):
                     
                    queryset = queryset.filter(form_status="Incomplete")
                     
                else:
                     return Response(
    {"detail": "You do not have permission to access this."},
    status=status.HTTP_403_FORBIDDEN
)

            # ---------------- All ----------------
            elif type_filter == "All":
                if user.has_perm("core.view_all_rental_deals"):
                    print("entered all block")
                    queryset = queryset.filter(form_status="Complete") 
                    print(queryset)
                    # print(f"Queryset count after filter: {queryset.count()}")
                else:
                    return Response({"detail": "You do not have permission to access this."}, status=status.HTTP_403_FORBIDDEN)
                
                
            if role == "Agent" or user_role == "Agent":
                queryset = queryset.filter(submitted_by_user=user)
                if type_filter == "rejected": 
                    queryset = queryset.filter(Q(is_approved_rejected="R") | Q(manager_approved_rejected="R"), form_status="Complete")
                elif type_filter == "approved":
                    queryset = queryset.filter(Q(is_approved_rejected="A") , form_status="Complete")

            elif (role == "Admin" or user_role == "Admin") and type_filter == "draft":
                queryset = queryset.filter(created_by=user.email)
            else:
                role = "superadmin" 




        # print(queryset)
        order = request.data.get("order", [{}])[0]  # ⬅️ Use raw request.data
        # print("Order parameter:", order)
 
        column_index = order.get("column")
        direction = order.get("dir")
        # print(f"Column index: {column_index}, Direction: {direction}")
 
        column_mapping = {
            0: None,  # Action column (not orderable)
            1: "id",
            2: "reference_number",
            3: "deal_date",
            4: "unit_details",
            5: "building_name",
            6: "project_name",
            7: "rental_price",
            8: "deal_start_date",
            9: "deal_end_date",
            10: "submitted_date"
           
        }
 
        if column_index is not None and direction:
            try:
                column_index = int(column_index)
                column_name = column_mapping.get(column_index)
                # print(f"Mapped column name: {column_name}")
 
                if column_name:
                    order_expression = column_name if direction == "asc" else f"-{column_name}"
                    print("Ordering expression:", order_expression)
 
                    queryset = queryset.order_by(order_expression)
                    print("✅ Ordering applied. SQL:", str(queryset.query))
                    for obj in queryset[:5]:
                        print("➡️", obj.id, getattr(obj, column_name.strip("-"), None))
                else:
                    pass
                    # print("❌ No mapped column for given index:", column_index)
            except Exception as e:
                # print(f"⚠️ Ordering error: {str(e)}")
                pass

         
       


        # Date range filter
        if data.get("from_date"):
            # print( "thsiiis from_data" , data.get("from_date"))
            queryset = queryset.filter(date__gte=data.get("from_date"))
        if data.get("to_date"):
            queryset = queryset.filter(date__lte=data.get("to_date"))

        # Pagination
        start = int(data.get("start") )  # Default to 0 if not provided
        length = int(data.get("length")) 
        print(start , length) # Default to 10 if not provided

        if length != -1:
            paginated = list(queryset[start:start + length])
            # Get total count from a separate count query only if needed
            total_count = queryset.count() if start > 0 or len(paginated) == length else len(paginated)
        else:
            paginated = list(queryset)
            total_count = len(paginated)

        print(queryset)
        print(paginated)
 

        data = request.data.copy()  # Copy the original data to include in the responseda
        data.pop('csrfmiddlewaretoken', None)

        serializer = DealSerializerfordatatable(paginated, many=True, context={'request': request})
        response_data = {
            "draw": data.get("draw") ,  # Ensure draw is an integer
            "recordsTotal": total_count,
            "recordsFiltered": total_count,
            "data": serializer.data,
            # "input": data   
              # original input back
        } 

        return Response(response_data, status= status.HTTP_200_OK)
    # // create deal
 
   
    @action(detail=False, methods=['post'], url_path='create-deal')
    def create_deal(self, request):
        if not request.user.has_perm("core.add_rentaldeals"):
            return Response({"detail": "You do not have permission to access this."}, status=status.HTTP_403_FORBIDDEN)

        logger.info(
            "create_deal called: user=%s id=%s",
            getattr(request.user, "email", None),
            getattr(request.user, "id", None),
        )

        updated_files = {}
        base_field_name = ""
        removed_clean_dict = {}
        mutable_data = request.data.dict().copy()
        print(request.user)
        print(request.user.id)
        print(mutable_data)
        # rental_deal = get_object_or_404(RentalDeals, pk=pk)
        path = f"rental/referencenumber_CP/{mutable_data['reference_number'].strip()}"
        for key in request.FILES.keys():
            base_field_name = key.rstrip("[]")  # Remove [] suffix if present
            print("base_field_name", base_field_name)
            files = request.FILES.getlist(key)

        

            # Get existing value from the DB field (comma-separated filenames)
            # existing_value = getattr(rental_deal, base_field_name, "")
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
            reference_number = mutable_data.get("reference_number").strip()
            path_folder = f"rental/referencenumber_CP/{reference_number}"

            # existing_value = getattr(rental_deal, base_field_name, "")
            # existing_files = existing_value.split(",") if existing_value else []

            # updated_existing_files = []

      

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
                else :
                    logger.error(
                        "Failed to upload file %s for field %s reference=%s user=%s",
                        filename,
                        base_field_name,
                        reference_number,
                        getattr(request.user, "email", None),
                    )
                    return Response({"detail": f"Failed to upload file {filename}. Please try again.uploading"} , status=status.HTTP_400_BAD_REQUEST)

            # ✅ Combine and update mutable_data + DB dict
            combined_files =   new_file_names
            combined_str = ",".join(combined_files)

            # mutable_data[base_field_name] = combined_str
            final_updated_values[base_field_name] = combined_str



        for base_field_name, combined_str in final_updated_values.items():
            mutable_data[base_field_name] = combined_str 
            print(f"Updated mutable_data[{base_field_name}]:", mutable_data[base_field_name])

            


        

        


        # userobj = Users.objects.filter(pk = request.user.id)

        print(f"DEBUG: save_as received: {mutable_data.get('save_as')}") # <--- ADD THIS
        if mutable_data.get('save_as') == "create-deal":
            mutable_data['form_status'] = "Complete"
            mutable_data['submitted_date']= date.today()
        else:
            mutable_data['form_status'] = "Incomplete"
        print(f"DEBUG: form_status set to: {mutable_data['form_status']}") # <--- ADD THIS
        print(f"DEBUG: mutable_data before serializer: {mutable_data}") 



        
        # adding reference number to the table of recipts 
        if mutable_data.get('receipt_no'):

            if mutable_data['receipt_no'].isdigit():
                print("this is the receipt no", mutable_data['receipt_no'])
                Receipts.objects.filter(id=mutable_data['receipt_no']).update(deal_refer_no=mutable_data['reference_number'])
                Receipts.objects.filter(id=mutable_data['receipt_no']).update(status="Used")

                reccicpt = Receipts.objects.filter(id=mutable_data['receipt_no']).first()
                mutable_data['receipt_id'] = reccicpt.id
                mutable_data['receipt_no'] = reccicpt.receipt_number
                print("this is the receipt id", mutable_data['receipt_id'])
                print("this is the receipt no", mutable_data['receipt_no'])
            else:
                pass

        if mutable_data.get('receipt_no2'):
            if mutable_data['receipt_no2'].isdigit():
                print("this is the receipt no2", mutable_data['receipt_no2'])
                Receipts.objects.filter(id=mutable_data['receipt_no2']).update(deal_refer_no=mutable_data['reference_number'])
                Receipts.objects.filter(id=mutable_data['receipt_no2']).update(status="Used")

                reccicpt2 = Receipts.objects.filter(id=mutable_data['receipt_no2']).first()
                mutable_data['receipt_id2'] = reccicpt2.id
                mutable_data['receipt_no2'] = reccicpt2.receipt_number
                print("this is the receipt id2", mutable_data['receipt_id2'])
                print("this is the receipt no2", mutable_data['receipt_no2'])
            else:
                pass
        if mutable_data.get('receipt_no3'):
            if mutable_data['receipt_no3'].isdigit():
                print("this is the receipt no3", mutable_data['receipt_no3'])
                Receipts.objects.filter(id=mutable_data['receipt_no3']).update(deal_refer_no=mutable_data['reference_number'])
                Receipts.objects.filter(id=mutable_data['receipt_no3']).update(status="Used")

                reccicpt2 = Receipts.objects.filter(id=mutable_data['receipt_no3']).first()
                mutable_data['receipt_id3'] = reccicpt2.id
                mutable_data['receipt_no3'] = reccicpt2.receipt_number
                print("this is the receipt id3", mutable_data['receipt_id3'])
                print("this is the receipt no3", mutable_data['receipt_no3'])
            else:
                pass



        
        if not mutable_data.get('submitted_by_agent'):
            mutable_data['submitted_by_user'] = request.user.id
            mutable_data['submitted_by_agent'] = request.user.id

        else :
            mutable_data['submitted_by_user'] = mutable_data.get('submitted_by_agent')
           
            







        # mutable_data['submitted_by_user'] = request.user.id
        mutable_data['account'] = request.user.account_id
        # mutable_data['submitted_by_agent'] = request.user.id

        mutable_data['created_by'] = request.user.email
        mutable_data['created_at'] = now()

        print(f"multable data  acoount_id {mutable_data['account']}")
        print("mutalbel data before the serlizer", mutable_data)
        serializer = self.get_serializer(data=mutable_data)


        for key, value in final_updated_values.items():
            print(f"Final updated value - {key}: {value}")

        
       
        missing_files = []
        for base_field_name, files_str in final_updated_values.items():
            for fname in files_str.split(","):
                relative_path = f"rental/referencenumber_CP/{mutable_data['reference_number'].strip()}/{fname}"
                if not s3_file_exists(relative_path):
                    missing_files.append(fname)
        
        if missing_files:

            logger.error(
                "Missing files in S3 for reference=%s user=%s missing=%s",
                mutable_data.get("reference_number"),
                getattr(request.user, "email", None),
                missing_files,
            )
            return Response(
                {"detail": f"The following files are missing in S3: {', '.join(missing_files)} upload again"},
                status=status.HTTP_400_BAD_REQUEST
            )






        serializer.is_valid(raise_exception=True)
        serializer.save()
        logger.info(
            "Rental deal created reference_number=%s id=%s by=%s",
            serializer.data.get("reference_number"),
            serializer.data.get("id"),
            getattr(request.user, "email", None),)

        return Response(serializer.data, status=status.HTTP_200_OK)

    # edit the data 
    # @action(detail=True, methods=['get', 'post']) 
    # @permission_required('core.change_rentaldeals')
    def custom_update(self, request, pk=None):
        # print("Raw body:", request.body)
        if not request.user.has_perm("core.change_rentaldeals"):
            return Response({"detail": "You do not have permission to access this."}, status=status.HTTP_403_FORBIDDEN)
      
        rental_deal = get_object_or_404(RentalDeals, pk=pk)

        if request.method == 'GET':
            # ✅ Return current data (populate form)
            serializer = self.get_serializer(rental_deal)
            return Response(serializer.data)

        elif request.method == 'PUT':
            print("request data", request.data)
            print("✅ Files:", request.FILES) 
            # print("Keys in request.data:", request.data.keys())
            print("Files:", request.FILES.keys())
            rental_deal = get_object_or_404(RentalDeals, pk=pk)
            declared_file_fields = request.POST.get('__file_fields__', '').split(',')
            print("Declared file fields:", declared_file_fields)

            print("rental_deal", rental_deal)

            user = Users.objects.annotate(
            first_group_name=Subquery(
                Group.objects.filter(custom_user_set=OuterRef("pk"))
                .order_by("id")  # ensures consistent first group
                .values("name")[:1]  # take only the first group's name
            )
                ).get(id=request.user.id)

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
                existing_value_from_db = getattr(rental_deal, base_field_name, "")
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
                        filepath = f"/rental/referencenumber_CP/{rental_deal.reference_number}/{file_name}"

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
            path = f"rental/referencenumber_CP/{mutable_data['reference_number'].strip()}"
            for key in request.FILES.keys():
                base_field_name = key.rstrip("[]")  # Remove [] suffix if present
                print("base_field_name", base_field_name)
                files = request.FILES.getlist(key)
 
            

                # Get existing value from the DB field (comma-separated filenames)
                # existing_value = getattr(rental_deal, base_field_name, "")
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
                reference_number = mutable_data.get("reference_number").strip()
                path_folder = f"rental/referencenumber_CP/{reference_number}"

                existing_value = getattr(rental_deal, base_field_name, "")
                existing_files = existing_value.split(",") if existing_value else []

                updated_existing_files = []

                # ✅ Remove files if present in removed_clean_dict
                files_to_remove = removed_clean_dict.get(base_field_name, [])
                for file_name in existing_files:
                    file_name = file_name.strip()
                    if file_name in files_to_remove:
                        relative_path = f"{path_folder}/{file_name}"
                        # is_deleted = delete_from_s3(relative_path)
                        # logger.info("delete_from_s3 called for %s result=%s", relative_path, is_deleted)
                        # if is_deleted:
                        #     updated_existing_files.append(file_name)  # keep if deletion failed
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
                        logger.info("Uploaded file added: %s for field %s", filename, base_field_name)

                    else :
                        logger.error("Failed to upload file %s for field %s reference=%s user=%s", filename, base_field_name, reference_number, getattr(request.user, "email", None))

                        return Response({"detail": f"Failed to upload file {filename}. Please try again.uploading"} , status=status.HTTP_400_BAD_REQUEST)

                # ✅ Combine and update mutable_data + DB dict
                combined_files = updated_existing_files + new_file_names
                combined_str = ",".join(combined_files)

                # mutable_data[base_field_name] = combined_str
                final_updated_values[base_field_name] = combined_str



            for base_field_name, combined_str in final_updated_values.items():
                mutable_data[base_field_name] = combined_str 
                print(f"Updated mutable_data[{base_field_name}]:", mutable_data[base_field_name])



            print("user role is", user.first_group_name) 
            user_role = user.first_group_name or ""
            role = user_role.split("-", 1)[1] if "-" in user_role else user_role
            print(user_role)
            print(role)

            if mutable_data.get('save_as') == "update-deal":
                mutable_data['form_status'] = "Complete"
                is_submitted_date = getattr(rental_deal, 'submitted_date' , "")
                form_status = getattr(rental_deal, 'form_status' , "")
                print("form_status", form_status)
                print("is_submitted_date", is_submitted_date)


                if (not is_submitted_date and role in ["Agent"] ) : 
                    print("submitted date already set so not updating", is_submitted_date)
                    mutable_data['submitted_date']= date.today()
                           
                    # this the re submitted date block to handle rejection and  resubbmission
                elif (form_status == "Incomplete" and role in ["Agent"] and is_submitted_date) :
                     mutable_data['submitted_date']= date.today()
                elif is_submitted_date and role in ["Agent"]:
                    mutable_data['re_submitted_date']= date.today()
                    print("this is resubmitted date block", mutable_data['re_submitted_date'])
                    mutable_data['is_approved_rejected'] = "P"  # set to pending on resubmission
                    mutable_data['manager_approved_rejected'] = "P"  # set to pending on resubmission      
 
            else:
                mutable_data['form_status'] = "Incomplete"
            print(f"DEBUG: form_status set to: {mutable_data['form_status']}")

            if mutable_data.get('receipt_no') is not None:
                get_receipt_no_db = getattr(rental_deal, 'receipt_no', "")
                get_receipt_id_db = getattr(rental_deal, 'receipt_id', "")
                print("get_receipt_no_db", get_receipt_no_db)
                print("get_receipt_id_db", get_receipt_id_db)

                receipt_value = str(mutable_data.get('receipt_no')).strip()

                if receipt_value.isdigit():
                    if str(get_receipt_id_db) != receipt_value:
                        if str(get_receipt_id_db).isdigit():
                            Receipts.objects.filter(id=get_receipt_id_db).update(status="Unused", deal_refer_no="")

                        print("this is the receipt no", receipt_value)
                        Receipts.objects.filter(id=receipt_value).update(deal_refer_no=mutable_data['reference_number'])
                        Receipts.objects.filter(id=receipt_value).update(status="Used")

                    reccicpt = Receipts.objects.filter(id=receipt_value).first()
                    if reccicpt:
                        mutable_data['receipt_id'] = reccicpt.id
                        mutable_data['receipt_no'] = reccicpt.receipt_number
                else:
                    if receipt_value in ["Null", "No Commission", ""]:
                        if str(get_receipt_id_db).isdigit():
                            Receipts.objects.filter(id=get_receipt_id_db).update(status="Unused", deal_refer_no="")
                        mutable_data['receipt_id'] = 0
                        mutable_data['receipt_no'] = receipt_value

            if mutable_data.get('receipt_no2') is not None:
                get_receipt_no2_db = getattr(rental_deal, 'receipt_no2', "")
                get_receipt_id2_db = getattr(rental_deal, 'receipt_id2', "")
                print("get_receipt_no2_db", get_receipt_no2_db)
                print("get_receipt_id2_db", get_receipt_id2_db)

                receipt_value2 = str(mutable_data.get('receipt_no2')).strip()

                if receipt_value2.isdigit():
                    if str(get_receipt_id2_db) != receipt_value2:
                        if str(get_receipt_id2_db).isdigit():
                            Receipts.objects.filter(id=get_receipt_id2_db).update(status="Unused", deal_refer_no="")

                        print("this is the receipt no2", receipt_value2)
                        Receipts.objects.filter(id=receipt_value2).update(deal_refer_no=mutable_data['reference_number'])
                        Receipts.objects.filter(id=receipt_value2).update(status="Used")

                    reccicpt2 = Receipts.objects.filter(id=receipt_value2).first()
                    if reccicpt2:
                        mutable_data['receipt_id2'] = reccicpt2.id
                        mutable_data['receipt_no2'] = reccicpt2.receipt_number
                else:
                    if receipt_value2 in ["Null", "No Commission", ""]:
                        if str(get_receipt_id2_db).isdigit():
                            Receipts.objects.filter(id=get_receipt_id2_db).update(status="Unused", deal_refer_no="")
                        mutable_data['receipt_id2'] = 0
                        mutable_data['receipt_no2'] = receipt_value2
            if mutable_data.get('receipt_no3') is not None:
                get_receipt_no3_db = getattr(rental_deal, 'receipt_no3', "")
                get_receipt_id3_db = getattr(rental_deal, 'receipt_id3', "")
                print("get_receipt_no3_db", get_receipt_no3_db)
                print("get_receipt_id3_db", get_receipt_id3_db)

                receipt_value3 = str(mutable_data.get('receipt_no3')).strip()

                if receipt_value3.isdigit():
                    if str(get_receipt_id3_db) != receipt_value3:
                        if str(get_receipt_id3_db).isdigit():
                            Receipts.objects.filter(id=get_receipt_id3_db).update(status="Unused", deal_refer_no="")

                        print("this is the receipt no3", receipt_value3)
                        Receipts.objects.filter(id=receipt_value3).update(deal_refer_no=mutable_data['reference_number'])
                        Receipts.objects.filter(id=receipt_value3).update(status="Used")

                    reccicpt3 = Receipts.objects.filter(id=receipt_value3).first()
                    if reccicpt3:
                        mutable_data['receipt_id3'] = reccicpt3.id
                        mutable_data['receipt_no3'] = reccicpt3.receipt_number
                else:
                    if receipt_value3 in ["Null", "No Commission", ""]:
                        if str(get_receipt_id3_db).isdigit():
                            Receipts.objects.filter(id=get_receipt_id3_db).update(status="Unused", deal_refer_no="")
                        mutable_data['receipt_id3'] = 0
                        mutable_data['receipt_no3'] = receipt_value3
            
            if mutable_data.get("is_approved_rejected") and mutable_data.get("is_approved_rejected") in ["A", "R", "F"]:
                mutable_data['approved_rejected_by'] = request.user.email


            mutable_data['updated_by'] = request.user.email
            mutable_data['updated_at'] = now()

            


# if admin crea ting the deal on behalf of agent user willbe agent name if  agent creating deal user will be user name
            if not mutable_data.get('submitted_by_agent'):
                mutable_data['submitted_by_user'] = request.user.id
                mutable_data['submitted_by_agent'] = request.user.id
            else :
                mutable_data['submitted_by_user'] = mutable_data.get('submitted_by_agent')

            mutable_data['submitted_by_agent'] = request.user.id

            print("mutable_data", mutable_data)

            print("Before saving serializer data:", mutable_data.keys())
            # Now pass this updated data to serializer


            print("final UPdate values are " , final_updated_values)
            for key, value in final_updated_values.items():
                print(f"Final updated value - {key}: {value}")
                logger.debug("Final updated value - %s: %s", key, value)


            
            
            missing_files = []
            for base_field_name, files_str in final_updated_values.items():
                for fname in files_str.split(","):
                    print("Checking file name for the this field:", fname)
                    logger.info("checking file name %s", fname)
                    if fname.strip():
                        relative_path = f"rental/referencenumber_CP/{mutable_data['reference_number'].strip()}/{fname}"
                        logger.info("checking hte path send to s3 %s", relative_path)
                        if not s3_file_exists(relative_path):
                            missing_files.append(fname)
                
            if missing_files:
                logger.error("Missing files before update for rental id=%s missing=%s", rental_deal.pk, missing_files)

                return Response(
                    {"detail": f"The following files are missing in S3: {', '.join(missing_files)} upload again"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer = self.get_serializer(rental_deal, data=mutable_data, partial=True)

            # serializer = self.get_serializer(rental_deal, data=request.data, partial=True)

                # ✅ Update data from form
                # serializer = self.get_serializer(rental_deal, data=request.data, partial=True)
                
            if serializer.is_valid():
                print("Before saving serializer data:", mutable_data.keys())
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # update the fields      entered in finance system
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
                if field_name not in [f.name for f in RentalDeals._meta.get_fields()]:
                    return Response({'status': 'error', 'message': 'Invalid field name'}, status=400)

# Update directly in DB
                RentalDeals.objects.filter(id=obj_id).update(**{field_name: value})

                updated_deal = RentalDeals.objects.get(id=obj_id)

                return Response({'status': 'success',"updated_value":  getattr(updated_deal, field_name) })

            except Exception as e:
                return Response({'status': 'error', 'message': str(e)}, status=400)

        return Response({'status': 'error', 'message': 'Invalid request'}, status=400)

       
    # delete the deal soft delete
    @action(detail=True, methods=['delete'], url_path='delete')
    def delete_deal(self, request, pk=None):
        if not request.user.has_perm("core.change_rentaldeals"):
            return Response({"detail": "You do not have permission to access this."}, status=status.HTTP_403_FORBIDDEN)
        instance = self.get_object()
        print("instance", instance)
        
        # Mark attached receipts as Unused
        receipt_ids = [instance.receipt_id, instance.receipt_id2, instance.receipt_id3]
        receipt_ids = [rid for rid in receipt_ids if str(rid).isdigit() and int(rid) > 0]  # Filter out null/zero values
        if receipt_ids:
            Receipts.objects.filter(id__in=receipt_ids).update(status='Unused', deal_refer_no='')
        
        RentalDeals.objects.filter(pk=instance.pk).update(is_deleted='Y')
        RentalDeals.objects.filter(pk=instance.pk).update(reference_number= instance.reference_number+"D")
        print("instance", instance)
        return Response({'detail': 'Rental deal deleted'}, status=status.HTTP_200_OK)
    
    # recipt helper function 
    

    
    # view the rental deal
    @action(detail=True, methods=['get'], url_path='view')
    def view_rental_deal(self, request, pk=None):

        logger.info("Rental deal view is opened successfully")
        logger.error("Something went wrong")

        def get_receipt_info(receipt_no):
            print(receipt_no)
            """
            Returns (receipt_no_output, receipt_id)
            based on your business logic.
            """
            if receipt_no in ["Null", "", None]:
                return "Null", ""

            elif receipt_no == "No Commission":
                return "No Commission", ""

            # Find receipt
            else:
                rec = Receipts.objects.filter(receipt_number=receipt_no).first()
                if rec:
                    return rec.receipt_number, rec.id
             

            return "", ""




        rental_deal = get_object_or_404(RentalDeals, pk=pk)


        print(rental_deal.receipt_no,"this is the recipt no")


        serializer = DealSerializer(rental_deal,context={'request': request})
        aws_url = settings.AWS_URL+"rental/referencenumber_CP/"
        # return HttpResponse("hello this is view page")
        # if not rental_deal.receipt_no:
        #     recipt_no = None
        # else:
        #     recipt_no = Receipts.objects.filter(id=rental_deal.receipt_no).first() 
        #     print(recipt_no.receipt_number , "this is recipt id ")

        receipt_no = (rental_deal.receipt_no or "").strip()   # NORMALIZE
        print(receipt_no, "normalized receipt_no")

        # CASE 1: empty or Null
        if receipt_no in ["", "Null"]:
            recipt_no = "Null"
            recipt_id = ""

        # CASE 2: No Commission
        elif receipt_no == "No Commission":
            recipt_no = "No Commission"
            recipt_id = ""

        # CASE 3: Valid numeric receipt
        else:
            recipt = Receipts.objects.filter(receipt_number=receipt_no).first()
            if recipt:
                recipt_no = recipt.receipt_number
                recipt_id = recipt.id
            else:
                recipt_no = ""
                recipt_id = ""



                
        recipt_no_1, recipt_id_1 = get_receipt_info(rental_deal.receipt_no)
        # Receipt No 2
        recipt_no_2, recipt_id_2 = get_receipt_info(rental_deal.receipt_no2)

        # Receipt No 3
        recipt_no_3, recipt_id_3 = get_receipt_info(rental_deal.receipt_no3)


        return render(request, 'home/rentaldealview.html', {'rentaldeal': serializer.data, 'aws_base_url' : aws_url, "recipt_no":recipt_no  , "recipt_id":recipt_id ,
        "recipt_no_2":recipt_no_2 , "recipt_id_2":recipt_id_2 ,
        "recipt_no_3":recipt_no_3 , "recipt_id_3":recipt_id_3
        })
    
    # submitted by user dropdown we arenot using this
    def submitted_by_user_dropdown(self, request):
        """
        Custom action to get the user who submitted the deal.
        """
        try:
            agent_group = Group.objects.get(name="Agent")  # Adjust group name if needed
            agents = Users.objects.filter(is_active=True)
        except Group.DoesNotExist:
            agents = Users.objects.none()

        serializer = AgentDropdownSerializer(agents, many=True)
        return Response(serializer.data)
    
    # receipt dropdown 
    def receipt_drop_down(self, request):
        reciepts = Receipts.objects.all()
        return Response(ReceiptDropdownSerilizer(reciepts,many=True).data)
    
    # tenancy contact Generation  
    def download_tenancey_contact_pdf(self,request, pk =None):
        rental_deal = RentalDeals.objects.get(pk=pk) 
        deal = DealSerializer(rental_deal,context={'request': request})
        print(deal.data, "this is pdf")
        html_string = render_to_string('home/tenancy_contract_pdf.html', {'deal': deal.data})
        html = HTML(string=html_string, base_url=request.build_absolute_uri('/'))
        pdf_file = html.write_pdf()

        download = request.GET.get("download") == "1"
        disposition = 'attachment' if download else 'inline'

        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = f'{disposition}; filename="receipt_{rental_deal.reference_number}.pdf"'
        return response






Rental_DealViewSet_filter = Rental_DealViewSet.as_view({'post': 'datatable_filter' })
Rental_DealViewSet_view = Rental_DealViewSet.as_view({'get': 'view_rental_deal'})
Rental_DealViewSet_filter = Rental_DealViewSet.as_view({'post': 'datatable_filter'})
Rental_DealViewSet_create = Rental_DealViewSet.as_view({'post': 'create_deal'})
 
Rental_DealViewSet_delete = Rental_DealViewSet.as_view({'delete': 'delete_deal'})
 
Rental_DealViewSet_update = Rental_DealViewSet.as_view({
    'get': 'custom_update',
    'put': 'custom_update',
})
Rental_DealViewSet_finance_update = Rental_DealViewSet.as_view({'put': 'update_single_field'})
Rental_DealViewSet_agent_dropdown = Rental_DealViewSet.as_view({'get': 'submitted_by_user_dropdown'})
Rental_DealViewSet_receipts_dropdown = Rental_DealViewSet.as_view({'get': 'receipt_drop_down'})
Rental_DealViewSet_tenancey_contact  = Rental_DealViewSet.as_view({'get': 'download_tenancey_contact_pdf'})
 





def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        print(request)

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            print(f'{username , password}')
            # user = Users.objects.get(email=username)
            # print()
            # print(user.check_password(password))
            
            user =  authenticate(email = username , password = password)
            # user =  authenticate(username=username, password=password)
          
            print(user)
            
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, "accounts/login.html", {"form": form, "msg": msg})


def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)

            msg = 'User created - please <a href="/login">login</a>.'
            success = True

            # return redirect("/login/")

        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg": msg, "success": success})









@login_required(login_url="/login/")
@permission_required('auth.admin_dashboard_access',raise_exception=True)
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))
    
 

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))


# html for the all list of rental deals
@login_required(login_url="/login/") 
@permission_required("core.manage_rental_deals",raise_exception=True)
def all_rental_deals(request):
    """
    View to list all rental deals.
    """
    group = request.user.groups.first()
    print(group.name)
    return render(request, 'home/rentalall.html')


# // html forthe edit rental deal 
@login_required(login_url="/login/")
@permission_required('core.change_rentaldeals',raise_exception=True)
def edit_rental_deal_view(request, pk): 
    deal = RentalDeals.objects.get(pk=pk)
    aws_url = settings.AWS_URL+"rental/referencenumber_CP/"
    # account_id = request.user.account_id
    # try:
    #     agent_group = Group.objects.get(name="Agent")  # Adjust group name if needed
    #     agents = Users.objects.filter(is_active=True)
    # except Group.DoesNotExist:
    #         agents = Users.objects.none()
    
    agents = Users.objects.filter(is_active=True,  account_id = request.user.account_id)
    agents = AgentDropdownSerializer(agents, many=True).data

    group = request.user.groups.first().name
    print(group)
    role = group.split("-", 1)[1] if "-" in group else group
    # user_role = request.user.first_group_name or ""
    # role = user_role.split("-", 1)[1] if "-" in user_role else user_role

    print(role)
    reciepts1_used = deal.receipt_id if deal.receipt_id else ""
    reciepts2_used = deal.receipt_id2 if deal.receipt_id2 else ""      
    reciepts3_used = deal.receipt_id3 if deal.receipt_id3 else ""




    used_receipt_ids = [rid for rid in [reciepts1_used, reciepts2_used, reciepts3_used] if rid]
    if role == "Agent":
         
        
        reciepts_db = (
            Receipts.objects.filter(account_id=request.user.account_id, agent_id=request.user.id)
            .filter(Q(status="Unused") | Q(id__in=used_receipt_ids))
            .distinct()
            
        )
        print(reciepts_db)

    else:
        reciepts_db = Receipts.objects.filter(account_id = request.user.account_id).filter(Q(status="Unused") | Q(id__in=used_receipt_ids))


    receipts = ReceiptDropdownSerilizer(reciepts_db,many=True).data

    rental_data = {
        'agents': agents,
        'receipts': receipts
    }
       

    return render(request, 'home/editrentaldeal.html', {'deal_id': pk, 'aws_url': aws_url, 'reference_number': deal.reference_number , "rental_data" :  json.dumps(rental_data), })



# html for the create rental deal 
@login_required(login_url="/login/")
@permission_required('core.add_rentaldeals',raise_exception=True)
def create_rental_deal_view(request):
    """
    View to create a new rental deal.
    """
    print(request.user.account_id)

    # try:
    #     agent_group = Group.objects.all()  # Adjust group name if needed
    #     agents = Users.objects.filter(is_active=True)
    # except Group.DoesNotExist:
    #         agents = Users.objects.none()

    agents = Users.objects.filter(is_active=True , account_id = request.user.account_id)
    agents = AgentDropdownSerializer(agents, many=True).data

    reciepts_db = Receipts.objects.filter(account_id = request.user.account_id ,status= "Unused" , agent_id = request.user.id)
    receipts = ReceiptDropdownSerilizer(reciepts_db,many=True).data

    rental_data = { 
        'agents': agents,
        'receipts': receipts
    }
    # print(rental_data) # to check teh data 
    return render(request, 'home/createrentaldeal.html', { "rental_data" :  json.dumps(rental_data), } )






def home_redirect(request):
    return redirect('dashbroad') 




 