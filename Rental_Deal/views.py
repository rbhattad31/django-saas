import datetime
from fileinput import filename
from urllib import request
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
import re
from .Utilities import delete_from_s3, upload_file_to_full_s3_url


# Create your views here.
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from core.models import Users
from .forms import RentalDealForm, FinanceCommentForm

from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from core.models import RentalDeals,Users,Account,Receipts
from .serializers import DealSerializer, filterSerializer, AgentDropdownSerializer, ReceiptDropdownSerilizer
from .pagination import CustomPagination  
from rest_framework.pagination import PageNumberPagination  
# from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .forms import LoginForm, SignUpForm  # Add this import for LoginForm and SignUpForm
from datetime import datetime
from weasyprint import HTML
from django.template.loader import render_to_string

   

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

class Rental_DealViewSet(viewsets.ModelViewSet):
    queryset = RentalDeals.objects.all()
       # for default `list`, `retrieve`
    pagination_class = CustomPagination 
    
    def get_serializer_class(self):
        if self.action == 'datatable_filter':
            return filterSerializer
        return DealSerializer # Custom pagination class
    # filter bsed on input 
    @action(detail=False, methods=['post'] ,url_path='filter')
    def datatable_filter(self, request):
        print(request.data)
        print(request.data.get("order") ,"togetordering")
        user = Users.objects.get(email = request.user)
        print(request.user)
        account_id = user.account_id
        print( "account_from_request",request.user.account_id)
       

         

        queryset = RentalDeals.objects.filter(is_deleted="N", account_id = account_id)  # Filter out deleted deals

        serializer =  filterSerializer()
       
         
        user = Users.objects.get(email = request.user)
      
        

        
        print("Request data:", request.data)
        data = filterSerializer(data=request.data)
        data.is_valid(raise_exception=True)
        print()
        data = data.validated_data
        print("validated", data)


        user = request.user

        






        # Global search
        search_term = data.get("search", {}).get("value") or ''
        print(search_term , "point x1")
        combined_q_object = Q()
     
        combined_q_object |= Q(submitted_by_user__name__icontains=search_term)
        combined_q_object |= Q(reference_number__icontains=search_term)
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
            print(formatted_date_for_db)

            # Now add these date filters using the correctly formatted date.
            # For exact date match:
            combined_q_object |= Q(date=formatted_date_for_db)
            combined_q_object |= Q(deal_start_date=formatted_date_for_db)
            combined_q_object |= Q(deal_end_date=formatted_date_for_db)

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

        # Apply the combined Q object to the queryset
        print("point x2", queryset)
        queryset = queryset.filter(combined_q_object)
           

        # Field-specific filters
        filter_fields = [
            "reference_number", "unit_details", "building_name", "deal_type",
            "deal_status", "project_name", "owner_name", "tenant_name",
            "owner_mobile", "tenant_mobile"
        ]
        for field in filter_fields:
            print()
            value = data.get(field)
            if value:
                filter_kwargs = {f"{field}__icontains": value}
                queryset = queryset.filter(**filter_kwargs)

        # Filterationon types keyword
        type_filter = data.get("type")
        print(type_filter)
        role = user.groups.first().name if user.groups.exists() else ""
        print(role)


         
        
        if type_filter:
            if type_filter == 'pending':
                if account_id:
                    if role in [f'{account_id}-Manager', f'{account_id}-Agent',] or user.is_superuser:
                        queryset = queryset.filter(manager_approved_rejected='P', form_status='Complete')
                    else:
                        queryset = queryset.filter(is_approved_rejected='P', manager_approved_rejected='A', form_status='Complete')

            elif type_filter == 'approved':
                if role in [f'{account_id}-Manager', f'{account_id}-Agent',] or user.is_superuser:
                    queryset = queryset.filter(manager_approved_rejected='A', form_status='Complete')
                else:
                    queryset = queryset.filter(is_approved_rejected='A' , form_status='Complete')

            elif type_filter == 'rejected':
                if role in [f'{account_id}-Manager', f'{account_id}-Agent',] or user.is_superuser:
                    queryset = queryset.filter( manager_approved_rejected='R', form_status='Complete')
                else:
                     queryset = queryset.filter(is_approved_rejected='R' , form_status='Complete')
                


            elif type_filter == "waiting-finance" :
                queryset = queryset.filter(is_approved_rejected='F')

            elif type_filter == 'entered-finance':
                queryset = queryset.filter(is_entered_in_finance_system='1',form_status= "Complete")

            elif type_filter == "pending-finance" :
                queryset = queryset.filter(is_entered_in_finance_system='0' ,form_status = "Complete")

            elif type_filter == 'draft':
                queryset = queryset.filter(form_status='Incomplete',submitted_by_user=user)
        
            elif type_filter == "All" :
                queryset = queryset.filter(form_status = "Complete")  

            if role == 'Admin' and type_filter == 'draft':
                queryset = queryset.filter(created_by=user.email)

 
        print(queryset)
        order = request.data.get("order", [{}])[0]  # ⬅️ Use raw request.data
        print("Order parameter:", order)
 
        column_index = order.get("column")
        direction = order.get("dir")
        print(f"Column index: {column_index}, Direction: {direction}")
 
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
                print(f"Mapped column name: {column_name}")
 
                if column_name:
                    order_expression = column_name if direction == "asc" else f"-{column_name}"
                    print("Ordering expression:", order_expression)
 
                    queryset = queryset.order_by(order_expression)
                    print("✅ Ordering applied. SQL:", str(queryset.query))
                    for obj in queryset[:5]:
                        print("➡️", obj.id, getattr(obj, column_name.strip("-"), None))
                else:
                    print("❌ No mapped column for given index:", column_index)
            except Exception as e:
                print(f"⚠️ Ordering error: {str(e)}")

         
       


        # Date range filter
        if data.get("from_date"):
            print( "thsiiis from_data" , data.get("from_date"))
            queryset = queryset.filter(date__gte=data.get("from_date"))
        if data.get("to_date"):
            queryset = queryset.filter(date__lte=data.get("to_date "))

        # Pagination
        start = int(data.get("start") )  # Default to 0 if not provided
        length = int(data.get("length")) 
        print(start , length) # Default to 10 if not provided
        paginated = queryset[start:start + length]
        print("paginated", paginated)
        

        data = request.data.copy()  # Copy the original data to include in the responseda
        data.pop('csrfmiddlewaretoken', None)

        serializer =  DealSerializer(paginated, many=True,context={'request': request})
        response_data = {
            "draw": data.get("draw") ,  # Ensure draw is an integer
            "recordsTotal": queryset.count(),
            "recordsFiltered": queryset.count(),
            "data": serializer.data,
            # "input": data   
              # original input back
        } 

        return Response(response_data)

    # // create deal
    @action(detail=False, methods=['post'], url_path='create-deal')
    def create_deal(self, request):


        updated_files = {}
        base_field_name = ""
        removed_clean_dict = {}
        mutable_data = request.data.copy()
        print(request.user)
        print(request.user.id)
        print(mutable_data)
        # rental_deal = get_object_or_404(RentalDeals, pk=pk)
        path = f"rental/referencenumber_CP/{mutable_data['reference_number']}"
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
            reference_number = mutable_data.get("reference_number")
            path_folder = f"rental/referencenumber_CP/{reference_number}"

            # existing_value = getattr(rental_deal, base_field_name, "")
            # existing_files = existing_value.split(",") if existing_value else []

            # updated_existing_files = []

            # ✅ Remove files if present in removed_clean_dict
            # files_to_remove = removed_clean_dict.get(base_field_name, [])
            # for file_name in existing_files:
            #     file_name = file_name.strip()
            #     if file_name in files_to_remove:
            #         relative_path = f"{path_folder}/{file_name}"
            #         is_deleted = delete_from_s3(relative_path)
            #         if not is_deleted:
            #             updated_existing_files.append(file_name)  # keep if deletion failed
            #     else:
            #         updated_existing_files.append(file_name)

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

            


        

        


        # userobj = Users.objects.filter(pk = request.user.id)

        print(f"DEBUG: save_as received: {mutable_data.get('save_as')}") # <--- ADD THIS
        if mutable_data.get('save_as') == "create-deal":
            mutable_data['form_status'] = "Complete"
        else:
            mutable_data['form_status'] = "Incomplete"
        print(f"DEBUG: form_status set to: {mutable_data['form_status']}") # <--- ADD THIS
        print(f"DEBUG: mutable_data before serializer: {mutable_data}") 



        
        # adding reference number to the table of recipts 
        if mutable_data.get('receipt_no'):
            print("this is the receipt no", mutable_data['receipt_no'])
            Receipts.objects.filter(id=mutable_data['receipt_no']).update(deal_refer_no=mutable_data['reference_number'])
            Receipts.objects.filter(id=mutable_data['receipt_no']).update(status="Used")
        


        mutable_data['submitted_by_user'] = request.user.id
        mutable_data['account'] = request.user.account_id

        print(f"multable data  acoount_id {mutable_data['account']}")
        serializer = self.get_serializer(data=mutable_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    # edit the data 
    # @action(detail=True, methods=['get', 'post']) 
    def custom_update(self, request, pk=None):
        # print("Raw body:", request.body)
      
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

            #
            removed_fields = {
                key[:-8]: value.strip()
                for key, value in request.POST.items()
                if key.endswith('_removed') and value.strip()
}
            print("Removed fields:", removed_fields)

            mutable_data = request.data.copy()
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
            path = f"rental/referencenumber_CP/{mutable_data['reference_number']}"
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
                reference_number = mutable_data.get("reference_number")
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



                 
            # if mutable_data.get('save_as') == "update-deal":
            #     mutable_data['form_status'] = "Complete"
            # else:
            #     mutable_data['form_status'] = "Incomplete"
            # print(f"DEBUG: form_status set to: {mutable_data['form_status']}")

            print("mutable_data", mutable_data)
            # Now pass this updated data to serializer
            serializer = self.get_serializer(rental_deal, data=mutable_data, partial=True)

            # serializer = self.get_serializer(rental_deal, data=request.data, partial=True)

                # ✅ Update data from form
                # serializer = self.get_serializer(rental_deal, data=request.data, partial=True)
                
            if serializer.is_valid():
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
        instance = self.get_object()
        print("instance", instance)
        RentalDeals.objects.filter(pk=instance.pk).update(is_deleted='Y')
        print("instance", instance)
        return Response({'detail': 'Rental deal deleted'}, status=status.HTTP_200_OK)
    
    # view the rental deal
    @action(detail=True, methods=['get'], url_path='view')
    def view_rental_deal(self, request, pk=None):
        rental_deal = get_object_or_404(RentalDeals, pk=pk)


        print(rental_deal.receipt_no,"this is the recipt no")


        serializer = DealSerializer(rental_deal,context={'request': request})
        aws_url = settings.AWS_URL
        # return HttpResponse("hello this is view page")

        recipt_no = Receipts.objects.filter(id=rental_deal.receipt_no).first() 
        print(recipt_no.id , "this is recipt id ")



        return render(request, 'home/rentaldealview.html', {'rentaldeal': serializer.data, 'aws_base_url' : aws_url, "recipt_no":recipt_no})
    
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
def all_rental_deals(request):
    """
    View to list all rental deals.
    """
    return render(request, 'home/rentalall.html')


# // html forthe edit rental deal 
@login_required(login_url="/login/")
def edit_rental_deal_view(request, pk): 
    deal = RentalDeals.objects.get(pk=pk)
    aws_url = settings.AWS_URL
    # account_id = request.user.account_id
    # try:
    #     agent_group = Group.objects.get(name="Agent")  # Adjust group name if needed
    #     agents = Users.objects.filter(is_active=True)
    # except Group.DoesNotExist:
    #         agents = Users.objects.none()
    
    agents = Users.objects.filter(is_active=True,  account_id = request.user.account_id)
    agents = AgentDropdownSerializer(agents, many=True).data

    reciepts_db = Receipts.objects.filter(account_id = request.user.account_id , status= "Unused")
    receipts = ReceiptDropdownSerilizer(reciepts_db,many=True).data

    rental_data = {
        'agents': agents,
        'receipts': receipts
    }
       

    return render(request, 'home/editrentaldeal.html', {'deal_id': pk, 'aws_url': aws_url, 'reference_number': deal.reference_number , "rental_data" :  json.dumps(rental_data), })



# html for the create rental deal 
@login_required(login_url="/login/")
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

    reciepts_db = Receipts.objects.filter(account_id = request.user.account_id ,status= "Unused")
    receipts = ReceiptDropdownSerilizer(reciepts_db,many=True).data

    rental_data = { 
        'agents': agents,
        'receipts': receipts
    }
    # print(rental_data) # to check teh data 
    return render(request, 'home/createrentaldeal.html', { "rental_data" :  json.dumps(rental_data), } )





 




 