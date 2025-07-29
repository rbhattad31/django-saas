
 

import warnings
warnings.filterwarnings("ignore")
import datetime
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect


# Create your views here.
from django.contrib.auth import authenticate, login
# from .forms import LoginForm

from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from core.models import RentalProperties
from .serializers import AgentDropdownSerializer, DealSerializer,filterSerializer
# from .pagination import CustomPagination  
# from rest_framework.pagination import PageNumberPagination  
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
# from .forms import LoginForm, SignUpForm  # Add this import for LoginForm and SignUpForm
   

from django_filters import rest_framework as filters
from django.template import loader
from django import template
from django.urls import reverse
import os


from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
# --- this goes outside the ViewSet class ---

from django.shortcuts import render, get_object_or_404, redirect
# from .forms import PropertyForm
from .serializers import PropertySerializer  # You'll need to create this serializer
from rest_framework.views import APIView
from django.http import FileResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now
from datetime import datetime
from django.db.models import Max
from core.models import Users,RentalProperties  # Ensure this import exists
from .utils import upload_file_to_full_s3_url
from django.shortcuts import render, get_object_or_404, redirect
import time
import re
from django.contrib.auth.models import Group
from core.models import Users,ManagementReceipts
from .serializers import UsersSerializer,ManagementReceiptsFilterSerializer,ManagementReceiptsSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from weasyprint import HTML
import logging
logger = logging.getLogger(__name__)
import datetime






def dashboard_view(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % ('/login/', request.path))
    print("User authenticated:", request.user.is_authenticated)
    print("User:", request.user)
    print("Is anonymous:", request.user.is_anonymous)
    return render(request, 'home/index.html')


class UsersViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer

    def update(self, request, *args, **kwargs):
        print("DEBUG is_deleted:", request.data.get("is_deleted"))
        return super().update(request, *args, **kwargs)
    

class PropertyAPIView(APIView):
    def get(self, request, pk):
        property_obj = get_object_or_404(RentalProperties, pk=pk)
        serializer = PropertySerializer(property_obj)
        return Response(serializer.data)

    # def put(self, request, pk):
    #     print("DEBUG: PUT method triggered")
    #     print("DEBUG is_deleted:", request.data.get("is_deleted"))
    #     property_obj = get_object_or_404(RentalProperties, pk=pk)
    #     serializer = PropertySerializer(property_obj, data=request.data, partial=True)
        
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        print("DEBUG: PUT method triggered")
        print("DEBUG is_deleted:", request.data.get("is_deleted"))
        property_obj = get_object_or_404(RentalProperties, pk=pk)
        mutable_data = request.data.copy()
        updated_files = {}

        reference_number = mutable_data.get('reference_number') or property_obj.reference_number
        path = f"rental/referencenumber_CP/{reference_number}"

        print(f"🔍 STARTING UPDATE for Property ID: {pk}")
        print(f"📁 Reference Path: {path}")
        print(f"📥 FILE KEYS: {list(request.FILES.keys())}")
        print(f"📝 FORM DATA: {dict(request.data)}")

        # Define file fields
        file_fields = [
            'pms_contract', 'owner_passport_copy', 'pms_cheque_copy',
            'title_deed', 'kyc_form', 'screening'
        ]

        # Process file uploads
        if request.FILES:
            for key in request.FILES.keys():
                base_field_name = key.rstrip("[]")  # Handles pms_contract[] or pms_contract
                if base_field_name not in file_fields:
                    print(f"⚠️ Skipping invalid file field: {base_field_name}")
                    continue

                files = request.FILES.getlist(key)
                print(f"📂 Field: {base_field_name}, Files Count: {len(files)}")

                for file in files:
                    timestamp = int(time.time())
                    cleaned_name = re.sub(r"[,]+", " ", file.name)
                    filename = f"{base_field_name}{timestamp}_{cleaned_name}"
                    filepath = f"{path}/{filename}"

                    print(f"⬆️ Uploading file: {filename} to {filepath}")
                    is_uploaded = upload_file_to_full_s3_url(file, filepath)
                    if is_uploaded:
                        if base_field_name not in updated_files:
                            updated_files[base_field_name] = []
                        updated_files[base_field_name].append(filepath)
                        print(f"✅ Uploaded: {filename}")
                    else:
                        print(f"❌ Upload failed: {filename}")
                        return Response(
                            {"error": f"Failed to upload file: {filename}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR
                        )

            # Update mutable_data with new file paths
            for field in file_fields:
                removed_files = mutable_data.get(f"{field}_removed", "").split(",")
                existing = getattr(property_obj, field, "") or ""
                existing_files = existing.split(",") if existing else []
                existing_files = [f for f in existing_files if f and f not in removed_files]
                new_files = updated_files.get(field, [])
                combined_files = existing_files + new_files
                combined_str = ",".join(combined_files) if combined_files else ""
                mutable_data[field] = combined_str
                print(f"🔄 {field}: {combined_str}")

        # Validate required file fields
        required_file_fields = file_fields
        for field in required_file_fields:
            existing_value = getattr(property_obj, field, "") or ""
            new_value = mutable_data.get(field, existing_value)
            if not new_value and request.FILES.get(f"{field}[]") is None and not existing_value:
                print(f"❌ Validation failed: {field} is required")
                return Response(
                    {"error": f"{field} is required."},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Handle cheque dates
        cheque_dates = []
        for key in mutable_data.keys():
            if key.startswith('cheque_date['):
                date = mutable_data[key]
                if date:
                    cheque_dates.append(date)
        mutable_data['cheque_date'] = ' '.join(cheque_dates) if cheque_dates else ''

        # Update via serializer for non-file data
        serializer = PropertySerializer(property_obj, data=mutable_data, partial=True)
        if serializer.is_valid():
            serializer.save()
            # Update file fields directly on the model instance
            for field in file_fields:
                setattr(property_obj, field, mutable_data.get(field, ""))
            property_obj.save()
            serializer = PropertySerializer(property_obj)  # Refresh serializer with updated data
            print(f"✅ Saved instance: {serializer.data}")
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
   

# def edit_property_page(request, pk):
#     property_obj = get_object_or_404(RentalProperties, pk=pk)
    
#     if request.method == "POST":
#         form = PropertyForm(request.POST, request.FILES, instance=property_obj)
#         if form.is_valid():
#             form.save()
#             return redirect('rental-property-list')
    
#     form = PropertyForm(instance=property_obj)
    
#     return render(request, 'home/edit_property.html', {
#         'form': form,
#         'property': property_obj
#     })

def edit_property_page(request, pk):
    property_obj = get_object_or_404(RentalProperties, pk=pk)

    # if request.method == "POST":
    #     form = PropertyForm(request.POST, request.FILES, instance=property_obj)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('rental-property-list')

    # form = PropertyForm(instance=property_obj)

    # ✅ Fetch unique, cleaned receipt numbers
    receipt_nos_raw = RentalProperties.objects.values_list('receipt_no', flat=True).distinct()
    receipt_nos = [rcpt.strip() for rcpt in receipt_nos_raw if rcpt and rcpt.strip()]

    return render(request, 'home/edit_property.html', {
        # 'form': form,
        'property': property_obj,
        'receipt_nos': receipt_nos   # ✅ Pass to template
    })




def download_receipt(request, pk):
    property = get_object_or_404(RentalProperties, pk=pk)
    if property.receipt_file:  # Assuming you have a FileField for receipts
        file_path = property.receipt_file.path
        if os.path.exists(file_path):
            return FileResponse(open(file_path, 'rb'), content_type='application/pdf')
    # Fallback if no file exists
    return HttpResponse("Receipt not found", status=404)



# @csrf_exempt
# def rental_property_create(request):
#     if request.method == 'POST':
#         is_draft = request.path == '/save-draft/' or 'save_draft' in request.POST
#         rental = RentalProperties.objects.create(
#             deal_submitted_by=request.POST.get('deal_submitted_by'),
#             reference_number=request.POST.get('reference_number'),
#             building_name=request.POST.get('building_name'),
#             pms_price=request.POST.get('pms_price'),
#             pm_end_date=request.POST.get('pm_end_date'),
#             tenancy_end_date=request.POST.get('tenancy_end_date'),
#             deal_date=request.POST.get('deal_date'),
#             project_name=request.POST.get('project_name'),
#             unit_no=request.POST.get('unit_no'),
#             pm_start_date=request.POST.get('pm_start_date'),
#             tenancy_start_date=request.POST.get('tenancy_start_date'),

#             owner_name=request.POST.get('owner_name'),
#             owner_mobile=request.POST.get('owner_mobile'),
#             owner_nationality=request.POST.get('owner_nationality'),
#             owner_source=request.POST.get('owner_source'),
#             owner_email=request.POST.get('owner_email'),

#             agency_name=request.POST.get('agency_name'),
#             agent_brn=request.POST.get('agent_brn'),
#             agent_name=request.POST.get('agent_name'),
#             agent_phone=request.POST.get('agent_phone'),
#             agent_email=request.POST.get('agent_email'),

#             number_of_cheque=request.POST.get('number_of_cheque'),
#             cheque_date=request.POST.get('cheque_date'),

#             total_commission=request.POST.get('total_commission'),
#             net_commission=request.POST.get('net_commission'),
#             agent1_commission=request.POST.get('agent1_commission'),
#             agent2_commission=request.POST.get('agent2_commission'),
#             agent3_commission=request.POST.get('agent3_commission'),
#             agent_comments=request.POST.get('agent_comments'),
#             receipt_no=request.POST.get('receipt_no'),
#             less_outside_commission=request.POST.get('less_outside_commission'),
#             classic=request.POST.get('classic'),
#             agent1_commission_value=request.POST.get('agent1_commission_value'),
#             agent2_commission_value=request.POST.get('agent2_commission_value'),
#             agent3_commission_value=request.POST.get('agent3_commission_value'),
#             admin_comments=request.POST.get('admin_comments'),
#             kyc_number=request.POST.get('kyc_number'),
#             aml=request.POST.get('aml'),
#             approve_reject=request.POST.get('approve_reject'),

#             is_draft=is_draft,
#         )

#         rental.pms_contract = request.FILES.get('pms_contract')
#         rental.title_deed = request.FILES.get('title_deed')
#         rental.poa_copy = request.FILES.get('poa_copy')
#         rental.kyc_form = request.FILES.get('kyc_form')
#         rental.owner_passport_copy = request.FILES.get('owner_passport_copy')
#         rental.pms_cheque_copy = request.FILES.get('pms_cheque_copy')
#         rental.poa_pp = request.FILES.get('poa_pp')
#         rental.key_hand_over_form = request.FILES.get('key_hand_over_form')
#         rental.screening = request.FILES.get('screening')
#         rental.screening_comments = request.POST.get('screening_comments')
#         rental.save()

#         if is_draft:
#             return redirect('draft-property-list')
#         else:
#             return redirect('rental-property-list')

#     return render(request, 'home/create_property.html')

@csrf_exempt
def rental_property_create(request):
    if request.method == 'POST':
        is_draft = request.path == '/save-draft/' or 'save_draft' in request.POST
        is_create = 'create_property' in request.POST

        last_sno = RentalProperties.objects.aggregate(Max('deal_sno'))['deal_sno__max'] or 0
        new_sno = last_sno + 1
        is_entered_value = request.POST.get('is_entered_in_finance_system') or '0'

        # Custom multi-file upload
        reference_number = request.POST.get('reference_number') or f"AUTO{new_sno}"
        s3_path = f"rental/referencenumber_CP/{reference_number}"

        uploaded_files = {}
        file_fields = [
            'pms_contract', 'title_deed', 'poa_copy', 'kyc_form',
            'owner_passport_copy', 'pms_cheque_copy', 'poa_pp',
            'key_hand_over_form', 'screening'
        ]

        for field in file_fields:
            uploaded_files[field] = ""
            files = request.FILES.getlist(field)
            saved_filenames = []
            for file in files:
                timestamp = int(time.time())
                cleaned_name = re.sub(r"[,]+", " ", file.name)
                filename = f"{field}{timestamp} {cleaned_name}"
                full_path = f"{s3_path}/{filename}"
                is_uploaded = upload_file_to_full_s3_url(file, full_path)
                if is_uploaded:
                    saved_filenames.append(filename)
            uploaded_files[field] = ",".join(saved_filenames)

        rental = RentalProperties.objects.create(
            deal_date=request.POST.get('deal_date'),
            reference_number=reference_number,
            project_name=request.POST.get('project_name'),
            building_name=request.POST.get('building_name'),
            unit_details=request.POST.get('unit_details'),
            pms_price=request.POST.get('pms_price'),
            pm_start_date=request.POST.get('pm_start_date'),
            pm_end_date=request.POST.get('pm_end_date'),
            tenancy_start_date=request.POST.get('tenancy_start_date'),
            tenancy_end_date=request.POST.get('tenancy_end_date'),

            owner_first_name=request.POST.get('owner_source'),
            owner_mobile=request.POST.get('owner_mobile'),
            owner_source=request.POST.get('owner_source'),
            owner_email=request.POST.get('owner_email'),

            agency_name=request.POST.get('agency_name'),
            agent_name=request.POST.get('agent_name'),
            brn=request.POST.get('agent_brn'),
            agent_phone=request.POST.get('agent_phone'),
            agent_email=request.POST.get('agent_email'),

            no_of_cheque=request.POST.get('no_of_cheque'),
            cheque_date=request.POST.get('cheque_date[]'),

            total_commission=request.POST.get('total_commission'),
            net_commission=request.POST.get('net_commission'),

            agent1=request.POST.get('agent1'),
            agent2=request.POST.get('agent2_commission'),
            agent3=request.POST.get('agent3_commission'),

            agent_comment=request.POST.get('agent_comments'),
            comments=request.POST.get('admin_comments'),

            receipt_no=request.POST.get('receipt_no'),
            less_outside_commission=request.POST.get('less_outside_commission'),
            classic=request.POST.get('classic'),

            screening_comments=request.POST.get('screening_comments'),
            kyc_number=request.POST.get('kyc_number'),
            is_property_aml=request.POST.get('is_property_aml'),
            is_approved_rejected=request.POST.get('approve_reject') or 'P',
            is_entered_in_finance_system=is_entered_value,
            submitted_by_user_id=request.user.id if request.user.is_authenticated else 0,

            deal_sno=new_sno,
            form_status='Incomplete' if is_draft else 'Complete',
            status='active',
            is_deleted='0',
            submitted_date=datetime.today().date(),
            manager_approved_rejected='0',
            created_at=now(),
            updated_at=now(),

            # File fields with uploaded values
            pms_contract=uploaded_files['pms_contract'],
            title_deed=uploaded_files['title_deed'],
            poa_copy=uploaded_files['poa_copy'],
            kyc_form=uploaded_files['kyc_form'],
            owner_passport_copy=uploaded_files['owner_passport_copy'],
            pms_cheque_copy=uploaded_files['pms_cheque_copy'],
            poa_pp=uploaded_files['poa_pp'],
            key_hand_over_form=uploaded_files['key_hand_over_form'],
            screening=uploaded_files['screening'],
        )

        # Redirect logic
        if is_create:
            return redirect(reverse('rental-property-list'))
        elif is_draft:
            return redirect(reverse('rental-property-draft'))
        else:
            return redirect(reverse('rental-property-list'))

    return render(request, 'home/create_property.html')

# ------------------- Auth Views -------------------



class Rental_PropertyViewSet(viewsets.ModelViewSet):
    queryset = RentalProperties.objects.all()
    serializer_class = filterSerializer  # for default `list`, `retrieve`
    # pagination_class = CustomPagination  # Custom pagination class

    permission_classes = [permissions.IsAuthenticated]

    # #Adding actions code 
    # @action(detail=True, methods=['get'], url_path='view')
    # def view_property(self, request, pk=None):
    #     property = get_object_or_404(RentalProperties, pk=pk)
    #     serializer = DealSerializer(property)
    #     return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        print("DEBUG is_deleted:", request.data.get("is_deleted"))  # Add this
        return super().update(request, *args, **kwargs)

    # def get_serializer_class(self):
    #     if self.action == 'create' or self.action == 'edit':
    #         return PropertySerializer
    #     return filterSerializer
    def get_serializer_class(self):
        if self.action in ['create', 'edit', 'custom_update']:
            return PropertySerializer
        return filterSerializer

    # @action(detail=False, methods=['get'], url_path='create-form')
    # def create_form(self, request):
    #     """Render the create property form."""
    #     form = PropertyForm()
    #     return render(request, 'home/create_property.html', {'form': form})
    
    @action(detail=False, methods=['get'], url_path='create-form')
    def create_form(self, request):
        
        from property_management_deals.models import Users 
        agents_raw = Users.objects.all()

        # Filter out users with blank/null/whitespace-only names
        agents = [agent for agent in agents_raw if agent.name and agent.name.strip()]

        print("---- Cleaned Agent Names ----")
        for agent in agents:
            print(agent.name.strip())
        print("-----------------------------")

        # Fetch unique, non-empty receipt numbers
        receipt_no = ManagementReceipts.objects.all()
       

        print("----- Valid Receipt Numbers -----")
        for rcpt in receipt_no:
            print(rcpt)
        print("----------------------------------")



        return render(request, 'home/create_property.html', {'form': form, 'agents': agents, 'receipt_nos': receipt_no})



    # @action(detail=False, methods=['post'], url_path='create')
    # def create(self, request):
    #     """Handle the creation of a new property."""
    #     serializer = PropertySerializer(data=request.data)
    #     print("request Data",request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # @action(detail=False, methods=['post'], url_path='create')
    # def create(self, request):
    #     """Handle the creation of a new property or saving as draft."""
    #     print("Request data for create", request.data)

    #     if request.data.get('save_as') == 'draft':
    #         required_fields = [
    #             'submitted_by_agent', 'deal_date', 'reference_number', 'project_name', 'building_name',
    #             'unit_details', 'pms_price', 'pm_start_date', 'pm_end_date', 'tenancy_start_date',
    #             'tenancy_end_date', 'owner_first_name', 'owner_source', 'owner_mobile', 'owner_email',
    #             'seller_nationality'
    #         ]
    #         for field in required_fields:
    #             if field not in request.data or not request.data[field]:
    #                 return Response(
    #                     {'success': False, 'message': f'{field} is required for draft.'},
    #                     status=status.HTTP_400_BAD_REQUEST
    #                 )

    #         # Prepare data for draft, excluding file fields
    #         draft_data = {
    #             field: request.data[field] for field in required_fields if field in request.data
    #         }
    #         draft_data['form_status'] = 'Incomplete'
    #         draft_data['is_approved_rejected'] = 'P'  # Default to Pending
    #         draft_data['is_entered_in_finance_system'] = '0'  # Default to No
    #         draft_data['is_deleted'] = 'N'  # Default to No

    #         try:
    #             instance = RentalProperties.objects.create(**draft_data)
    #             return Response(
    #                 {'success': True, 'message': 'Draft saved successfully', 'data': {'id': instance.id}},
    #                 status=status.HTTP_201_CREATED
    #             )
    #         except Exception as e:
    #             return Response(
    #                 {'success': False, 'message': f'Error saving draft: {str(e)}'},
    #                 status=status.HTTP_400_BAD_REQUEST
    #             )
    #     else:
    #         # For full submission, use the serializer with file validation
        
    #         serializer = PropertySerializer(data=request.data)
    #         if serializer.is_valid():
    #             serializer.save(form_status='Complete')  # Set form_status to Complete
    #             return Response(
    #                 {'success': True, 'data': serializer.data},
    #                 status=status.HTTP_201_CREATED
    #             )
    #         return Response(
    #             {'success': False, 'message': serializer.errors},
    #             status=status.HTTP_400_BAD_REQUEST
    #         )


    @action(detail=False, methods=['post'], url_path='create')
    def create(self, request):
        """Handle the creation of a new property or saving as draft."""
        print("Request data for create:", dict(request.data))
        print("File keys:", list(request.FILES.keys()))

        if request.data.get('save_as') == 'draft':
            required_fields = [
                'submitted_by_agent', 'deal_date', 'reference_number', 'project_name', 'building_name',
                'unit_details', 'pms_price', 'pm_start_date', 'pm_end_date', 'tenancy_start_date',
                'tenancy_end_date', 'owner_first_name', 'owner_source', 'owner_mobile', 'owner_email',
                'seller_nationality'
            ]
            for field in required_fields:
                if field not in request.data or not request.data[field]:
                    return Response(
                        {'success': False, 'message': f'{field} is required for draft.'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            # Prepare data for draft, excluding file fields
            draft_data = {
                field: request.data[field] for field in required_fields if field in request.data
            }
            draft_data['form_status'] = 'Incomplete'
            draft_data['is_approved_rejected'] = 'P'  # Default to Pending
            draft_data['is_entered_in_finance_system'] = '0'  # Default to No
            draft_data['is_deleted'] = 'N'  # Default to No

            try:
                instance = RentalProperties.objects.create(**draft_data)
                return Response(
                    {'success': True, 'message': 'Draft saved successfully', 'data': {'id': instance.id}},
                    status=status.HTTP_201_CREATED
                )
            except Exception as e:
                return Response(
                    {'success': False, 'message': f'Error saving draft: {str(e)}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            # For full submission, handle file uploads and validate
            data = {}  # Create a new dictionary instead of copying request.data
            updated_files = {}

            # Copy non-file fields from request.data
            for key in request.data:
                if key not in request.FILES:  # Exclude file fields
                    data[key] = request.data[key]

            reference_number = data.get('reference_number', '')
            if not reference_number:
                return Response(
                    {'success': False, 'message': 'reference_number is required for file uploads.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            path = f"rental/referencenumber_CP/{reference_number}"
            print(f"📁 Reference Path: {path}")
            print(f"📥 FILE KEYS: {list(request.FILES.keys())}")
            print(f"📝 FORM DATA: {dict(data)}")

            # Define file fields
            file_fields = [
                'pms_contract', 'owner_passport_copy', 'owner_eid_copy',
                'pms_cheque_copy', 'title_deed', 'poa_pp', 'poa_copy',
                'key_hand_over_form', 'kyc_form', 'screening'
            ]

            # Process file uploads
            for key in request.FILES.keys():
                base_field_name = key.rstrip("[]")
                if base_field_name not in file_fields:
                    print(f"⚠️ Skipping invalid file field: {base_field_name}")
                    continue

                files = request.FILES.getlist(key)
                print(f"📂 Field: {base_field_name}, Files Count: {len(files)}")

                for file in files:
                    timestamp = int(time.time())
                    cleaned_name = re.sub(r"[,]+", " ", file.name)
                    filename = f"{base_field_name}{timestamp}_{cleaned_name}"
                    filepath = f"{path}/{filename}"

                    print(f"⬆️ Uploading file: {filename} to {filepath}")
                    is_uploaded = upload_file_to_full_s3_url(file, filepath)
                    if is_uploaded:
                        if base_field_name not in updated_files:
                            updated_files[base_field_name] = []
                        updated_files[base_field_name].append(filepath)  # Store full S3 path
                        print(f"✅ Uploaded: {filename}")
                    else:
                        print(f"❌ Upload failed: {filename}")
                        return Response(
                            {"error": f"Failed to upload file: {filename}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR
                        )

            # Combine uploaded files into data
            for field in file_fields:
                new_files = updated_files.get(field, [])
                combined_str = ",".join(new_files) if new_files else ""
                data[field] = combined_str
                print(f"🔄 {field}: {combined_str}")

            # Handle cheque dates
            cheque_dates = []
            for key in data.keys():
                if key.startswith('cheque_date['):
                    date = data[key]
                    if date:
                        cheque_dates.append(date)
            data['cheque_date'] = ' '.join(cheque_dates) if cheque_dates else ''

            data["submitted_by_user_id"] = request.user.id
            data['submitted_date'] = datetime.date.today()


            ManagementReceipts.objects.filter(id = data['receipt_no']).update( deal_refer_no = data["reference_number"])

            # Validate and save via serializer
            serializer = PropertySerializer(data=data)
            if serializer.is_valid():
                serializer.save(form_status='Complete')  # Set form_status to Complete
                return Response(
                    {'success': True, 'data': serializer.data},
                    status=status.HTTP_201_CREATED
                )
            return Response(
                {'success': False, 'message': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
    @action(detail=True, methods=['get'], url_path='view')
    def view_property(self, request, pk=None):
        property = get_object_or_404(RentalProperties, pk=pk)
        serializer = DealSerializer(property )
        return render(request, 'home/view_property.html', {'property': serializer.data})

 
   
    @action(detail=True, methods=["post"], url_path="edit")
    def edit(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    


    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        # Your existing update method here
        property_obj = self.get_object()
        mutable_data = request.data.copy()
        updated_files = {}

        reference_number = mutable_data.get('reference_number') or property_obj.reference_number
        path = f"rental/referencenumber_CP/{reference_number}"

        print(f"🔍 STARTING UPDATE for Property ID: {kwargs.get('pk')}")
        print(f"📁 Reference Path: {path}")
        print(f"📥 FILE KEYS: {list(request.FILES.keys())}")
        print(f"📝 FORM DATA: {dict(request.data)}")

        # Define file fields
        file_fields = [
            'pms_contract', 'owner_passport_copy', 'pms_cheque_copy',
            'title_deed', 'kyc_form', 'screening'
        ]

        # Process file uploads
        if request.FILES:
            for key in request.FILES.keys():
                base_field_name = key.rstrip("[]")  # Handles pms_contract[] or pms_contract
                if base_field_name not in file_fields:
                    print(f"⚠️ Skipping invalid file field: {base_field_name}")
                    continue

                files = request.FILES.getlist(key)
                print(f"📂 Field: {base_field_name}, Files Count: {len(files)}")

                for file in files:
                    timestamp = int(time.time())
                    cleaned_name = re.sub(r"[,]+", " ", file.name)
                    filename = f"{base_field_name}{timestamp}_{cleaned_name}"
                    filepath = f"{path}/{filename}"

                    print(f"⬆️ Uploading file: {filename} to {filepath}")
                    is_uploaded = upload_file_to_full_s3_url(file, filepath)
                    if is_uploaded:
                        if base_field_name not in updated_files:
                            updated_files[base_field_name] = []
                        updated_files[base_field_name].append(filepath)
                        print(f"✅ Uploaded: {filename}")
                    else:
                        print(f"❌ Upload failed: {filename}")
                        return Response(
                            {"error": f"Failed to upload file: {filename}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR
                        )

            # Update mutable_data with new file paths
            for field in file_fields:
                removed_files = mutable_data.get(f"{field}_removed", "").split(",")
                existing = getattr(property_obj, field, "") or ""
                existing_files = existing.split(",") if existing else []
                existing_files = [f for f in existing_files if f and f not in removed_files]
                new_files = updated_files.get(field, [])
                combined_files = existing_files + new_files
                combined_str = ",".join(combined_files) if combined_files else ""
                mutable_data[field] = combined_str
                print(f"🔄 {field}: {combined_str}")

        # Validate required file fields
        required_file_fields = file_fields
        for field in required_file_fields:
            existing_value = getattr(property_obj, field, "") or ""
            new_value = mutable_data.get(field, existing_value)
            if not new_value and request.FILES.get(f"{field}[]") is None and not existing_value:
                print(f"❌ Validation failed: {field} is required")
                return Response(
                    {"error": f"{field} is required."},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Handle cheque dates
        cheque_dates = []
        for key in mutable_data.keys():
            if key.startswith('cheque_date['):
                date = mutable_data[key]
                if date:
                    cheque_dates.append(date)
        mutable_data['cheque_date'] = ' '.join(cheque_dates) if cheque_dates else ''

        # Update via serializer
        serializer = self.get_serializer(property_obj, data=mutable_data, partial=True)
        if serializer.is_valid():
            self.perform_update(serializer)
            print(f"✅ Saved instance: {serializer.data}")
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            print(f"❌ Serializer errors: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['put'], url_path='custom-update')
    def custom_update(self, request, pk=None):
        property_obj = get_object_or_404(RentalProperties, pk=pk)
        mutable_data = request.data.copy()
        updated_files = {}

        reference_number = mutable_data.get('reference_number') or property_obj.reference_number
        path = f"rental/referencenumber_CP/{reference_number}"

        print(f"🔍 STARTING CUSTOM UPDATE for Property ID: {pk}")
        print(f"📁 Reference Path: {path}")
        print(f"📥 FILE KEYS: {list(request.FILES.keys())}")
        print(f"📝 FORM DATA: {dict(request.data)}")

        # Define file fields
        file_fields = [
            'pms_contract', 'owner_passport_copy', 'owner_eid_copy',
            'pms_cheque_copy', 'title_deed', 'poa_pp', 'poa_copy',
            'key_hand_over_form', 'kyc_form', 'screening'
        ]

        # Process file uploads
        for key in request.FILES.keys():
            base_field_name = key.rstrip("[]")
            if base_field_name not in file_fields:
                print(f"⚠️ Skipping invalid file field: {base_field_name}")
                continue

            files = request.FILES.getlist(key)
            print(f"📂 Field: {base_field_name}, Files Count: {len(files)}")

            for file in files:
                timestamp = int(time.time())
                cleaned_name = re.sub(r"[,]+", " ", file.name)
                filename = f"{base_field_name}{timestamp}_{cleaned_name}"
                filepath = f"{path}/{filename}"

                print(f"⬆️ Uploading file: {filename} to {filepath}")
                is_uploaded = upload_file_to_full_s3_url(file, filepath)
                if is_uploaded:
                    if base_field_name not in updated_files:
                        updated_files[base_field_name] = []
                    updated_files[base_field_name].append(filepath)  # Store full S3 path
                    print(f"✅ Uploaded: {filename}")
                else:
                    print(f"❌ Upload failed: {filename}")
                    return Response(
                        {"error": f"Failed to upload file: {filename}"},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )

        # Handle removed files
        for field in file_fields:
            removed_files = mutable_data.get(f"{field}_removed", "").split(",")
            existing = getattr(property_obj, field, "") or ""
            existing_files = existing.split(",") if existing else []
            existing_files = [f for f in existing_files if f and f not in removed_files]
            new_files = updated_files.get(field, [])
            combined_files = existing_files + new_files
            combined_str = ",".join(combined_files) if combined_files else ""
            mutable_data[field] = combined_str
            print(f"🔄 {field}: {combined_str}")

        # Validate required file fields
        required_file_fields = [
            'pms_contract', 'owner_passport_copy', 'pms_cheque_copy',
            'title_deed', 'kyc_form', 'screening'
        ]
        for field in required_file_fields:
            existing_value = getattr(property_obj, field, "") or ""
            new_value = mutable_data.get(field, existing_value)
            if not new_value:
                print(f"❌ Validation failed: {field} is required")
                return Response(
                    {"error": f"{field} is required."},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Handle cheque dates
        cheque_dates = []
        for key in mutable_data.keys():
            if key.startswith('cheque_date['):
                date = mutable_data[key]
                if date:
                    cheque_dates.append(date)
        mutable_data['cheque_date'] = ' '.join(cheque_dates) if cheque_dates else ''

        # Update via serializer
        serializer = self.get_serializer(property_obj, data=mutable_data, partial=True)
        if serializer.is_valid():
            serializer.save()
            print("✅ Saved via serializer")
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            print(f"❌ Serializer errors: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
    @action(detail=True, methods=['delete'], url_path='delete')
    def delete_property(self, request, pk=None):

        property = get_object_or_404(RentalProperties, pk=pk)
        RentalProperties.objects.filter(pk=property.pk).update(is_deleted='Y')
        # property.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def edit_property_submit(request, pk):
        property_obj = get_object_or_404(RentalProperties, pk=pk)

        if request.method == "POST":
            property_obj.reference_number = request.POST.get("reference_number")
            property_obj.deal_date = request.POST.get("deal_date")
            property_obj.unit_details = request.POST.get("unit_details")
            property_obj.building_name = request.POST.get("building_name")
            property_obj.project_name = request.POST.get("project_name")
            property_obj.pms_price = request.POST.get("pms_price") or 0
            property_obj.pm_start_date = request.POST.get("pm_start_date")
            property_obj.pm_end_date = request.POST.get("pm_end_date")
            property_obj.tenancy_start_date = request.POST.get("tenancy_start_date")
            property_obj.tenancy_end_date = request.POST.get("tenancy_end_date")
            # Don't update submitted_date and status (they're readonly)
            # property_obj.submitted_date = request.POST.get("submitted_date")

            try:
                property_obj.save()
                return redirect("rental-deal")  # or wherever you want to go
            except Exception as e:
                # return render(request, "rental/edit_property.html", {
                #     "property": property_obj,
                #     "errors": str(e)
                # })
                return render(request, "home/edit_property.html", {
                "property": property_obj,
                "errors": str(e)
                })
            


    def submitted_by_user_dropdown(self, request):
        """
        Custom action to get the user who submitted the deal.
        """
        try:
            # agent_group = Group.objects.get(name="Agent")  # Adjust group name if needed
            agents = Users.objects.all()
            print(agents)
        except Group.DoesNotExist:
            agents = Users.objects.none()
 
        serializer = AgentDropdownSerializer(agents, many=True)
        return Response(serializer.data) 
    #end actions code 

    # @action(detail=False, methods=['post'] ,url_path='filter')
    # def datatable_filter(self, request):
    #     print("Request data:", request.data)
    #     data = filterSerializer(data=request.data)
    #     data.is_valid(raise_exception=True)
    #     data = data.validated_data
    #     print("validated", data)
        
    #     queryset = RentalProperties.objects.all()
    #     print("Queryset:",queryset)

    #     # Global search
    #     search_term = data.get("search", {}).get("value") or ''
    #     if search_term:
    #         queryset = queryset.filter(
    #             Q(reference_number__icontains=search_term) |
    #             Q(building_name__icontains=search_term) |
    #             Q(project_name__icontains=search_term)
    #         )
    #         print("pointx1", queryset)

    #     # Field-specific filters
    #     filter_fields = [
    #         "reference_no", "building_name", "unit_no", "project_name",
    #         "property_id", "approval_status", "deal_date_from", "deal_date_to",
    #         "pm_date_from", "pm_date_to","tenancy_date_from","tenancy_date_to"
    #     ]
    #     for field in filter_fields:
    #         value = data.get(field)
    #         if value:
    #             filter_kwargs = {f"{field}__icontains": value}
    #             queryset = queryset.filter(**filter_kwargs)

    #     # Filterationon types keyword
    #     deal_type = data.get("type")
         
    #     if deal_type == "All":
    #         queryset = queryset.filter(form_status="Complete")
        

    #     elif deal_type == "draft":
    #         queryset = queryset.filter(form_status="Incomplete")
            

    #     elif deal_type == "approved":
    #         queryset = queryset.filter(is_approved_rejected="A" )

    #     elif deal_type == "rejected":
    #         queryset = queryset.filter(is_approved_rejected="R" )

    #     elif deal_type == "waiting":
    #         queryset = queryset.filter( is_approved_rejected="F")

    #     elif deal_type == "pending":
            
    #         queryset = queryset.filter(is_approved_rejected="P")

    #     elif deal_type == "waiting-finance":
    #         queryset = queryset.filter(is_entered_in_finance_system="0")  
 
    #     elif deal_type == "entered-finance":
    #         queryset = queryset.filter(is_entered_in_finance_system="1")  
    #     else:
    #         return Response({"error": "Invalid deal type"}, status=400)
 


    #     # Date range filter
    #     if data.get("from"):
    #         queryset = queryset.filter(date__gte=data.get("from"))
    #     if data.get("to"):
    #         queryset = queryset.filter(date__lte=data.get("to"))

    #     # Pagination
    #     start = int(data.get("start") )  # Default to 0 if not provided
    #     length = int(data.get("length"))  # Default to 10 if not provided
    #     paginated = queryset[start:start + length]
    #     print("paginated", paginated)
        

    #     data = request.data.copy()  # Copy the original data to include in the responseda
    #     data.pop('csrfmiddlewaretoken', None)

    #     serializer =  DealSerializer(paginated, many=True ,  context = {"request":request})
    #     response_data = {
    #         "draw": int(data.get("draw") or 0),  # Ensure draw is an integer
    #         "recordsTotal": queryset.count(),
    #         "recordsFiltered": queryset.count(),
    #         "data": serializer.data,
    #         "input": data    # original input back
    #     }

    #     return Response(response_data)



    @action(detail=False, methods=['post'], url_path='filter')
    def datatable_filter(self, request):
        print("Request data:", request.data)
        print("Raw order in request.data:", request.data.get("order"))  # Debug raw order

        data = filterSerializer(data=request.data)
        data.is_valid(raise_exception=True)
        data = data.validated_data

        print("Validated data:", data)
        print("Order in validated data:", data.get("order"))  # Debug validated order

        queryset = RentalProperties.objects.all()
        print("Initial Queryset:", queryset)

        # Global search
        search_term = data.get("search", {}).get("value") or ''
        if search_term:
            queryset = queryset.filter(
                Q(reference_number__icontains=search_term) |
                Q(building_name__icontains=search_term) |
                Q(project_name__icontains=search_term)
            )
            print("After global search:", queryset)

        # Field-specific filters
        filter_fields = [
            "reference_no", "building_name", "unit_no", "project_name",
            "property_id", "approval_status", "deal_date_from", "deal_date_to",
            "pm_date_from", "pm_date_to", "tenancy_date_from", "tenancy_date_to"
        ]
        for field in filter_fields:
            value = data.get(field)
            if value:
                filter_kwargs = {f"{field}__icontains": value}
                queryset = queryset.filter(**filter_kwargs)
                print(f"Applied filter {field}:", queryset)

        # Filteration on types keyword
        deal_type = data.get("type")
        print("Deal type:", deal_type)
        if deal_type == "All":
            queryset = queryset.filter(form_status="Complete")
        elif deal_type == "draft":
            queryset = queryset.filter(form_status="Incomplete")
        elif deal_type == "approved":
            queryset = queryset.filter(is_approved_rejected="A")
        elif deal_type == "rejected":
            queryset = queryset.filter(is_approved_rejected="R")
        elif deal_type == "waiting":
            queryset = queryset.filter(is_approved_rejected="F")
        elif deal_type == "pending":
            queryset = queryset.filter(is_approved_rejected="P")
        elif deal_type == "waiting-finance":
            queryset = queryset.filter(is_entered_in_finance_system="0")
        elif deal_type == "entered-finance":
            queryset = queryset.filter(is_entered_in_finance_system="1")
        else:
            print("Invalid deal type received")
            return Response({"error": "Invalid deal type"}, status=400)
        print("After deal type filter:", queryset)

        # Date range filter
        if data.get("from"):
            queryset = queryset.filter(date__gte=data.get("from"))
            print("After from date filter:", queryset)
        if data.get("to"):
            queryset = queryset.filter(date__lte=data.get("to"))
            print("After to date filter:", queryset)

        # ✅ Ordering Logic
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
            7: "pms_price",
            8: "pm_start_date",
            9: "pm_end_date",
            10: "tenancy_start_date",
            11: "tenancy_end_date",
            12: "submitted_date",
            13: "status",
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

                    # Optional debug
                    for obj in queryset[:5]:
                        print("➡️", obj.id, getattr(obj, column_name.strip("-"), None))
                else:
                    print("❌ No mapped column for given index:", column_index)
            except Exception as e:
                print(f"⚠️ Ordering error: {str(e)}")

        # Pagination
        start = int(data.get("start", 0))
        length = int(data.get("length", 10))
        paginated = queryset[start:start + length]
        print("Paginated queryset:", paginated)

        # Prepare final response
        response_data = {
            "draw": int(data.get("draw", 0)),
            "recordsTotal": queryset.count(),
            "recordsFiltered": queryset.count(),
            "data": DealSerializer(paginated, many=True, context={"request": request}).data,
            "input": request.data.copy()
        }

        print("📦 Final response data preview:", response_data)
        return Response(response_data)



Rental_PropertyViewSet_filter = Rental_PropertyViewSet.as_view({
    'post': 'datatable_filter'
})
 


# def login_view(request):
#     form = LoginForm(request.POST or None)

#     msg = None

#     if request.method == "POST":

#         if form.is_valid():
#             username = form.cleaned_data.get("username")
#             password = form.cleaned_data.get("password")
#             user = authenticate(email=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect("/")
#             else:
#                 msg = 'Invalid credentials'
#         else:
#             msg = 'Error validating the form'

#     return render(request, "accounts/login.html", {"form": form, "msg": msg})
# def register_user(request):
#     msg = None
#     success = False

#     if request.method == "POST":
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             form.save()
#             email = form.cleaned_data.get("email")
#             raw_password = form.cleaned_data.get("password1")
#             user = authenticate(email=email, password=raw_password)
#             if user is not None:
#                 login(request, user)
#                 messages.success(request, 'User created and logged in successfully.')
#                 return redirect("/login/")
#             else:
#                 msg = 'User created but login failed. Please try logging in.'
#                 success = True
#         else:
#             msg = 'Form is not valid'
#     else:
#         form = SignUpForm()

#     return render(request, "accounts/register.html", {"form": form, "msg": msg, "success": success})



# @login_required(login_url="/login/")
# def index(request):
#     context = {'segment': 'index'}

#     html_template = loader.get_template('home/index.html')
#     return HttpResponse(html_template.render(context, request))


# @login_required(login_url="/login/")
# def pages(request):
#     context = {}
#     # All resource paths end in .html.
#     # Pick out the html file name from the url. And load that template.
#     try:

#         load_template = request.path.split('/')[-1]

#         if load_template == 'admin':
#             return HttpResponseRedirect(reverse('admin:index'))
#         context['segment'] = load_template

#         html_template = loader.get_template('home/' + load_template)
#         return HttpResponse(html_template.render(context, request))

#     except template.TemplateDoesNotExist:

#         html_template = loader.get_template('home/page-404.html')
#         return HttpResponse(html_template.render(context, request))

#     except:
#         html_template = loader.get_template('home/page-500.html')
#         return HttpResponse(html_template.render(context, request))



@login_required(login_url="/login/")
def all_rental_properties(request):
    print("User authenticated:", request.user.is_authenticated)
    print("User:", request.user)
    print("Is anonymous:", request.user.is_anonymous)
    print("User groups:", request.user.groups.all())
    """
    View to list all rental deals.
    """
    # return render(request, 'home/rentalall.html')
    path = request.path
    if path == '/rental-properties/draft/':
        properties = RentalProperties.objects.filter(form_status='Incomplete', is_deleted='0')
    else:
        properties = RentalProperties.objects.filter(is_deleted='0')
        
    
    return render(request, 'home/propertyall.html', {'properties': properties})

def draft_property_list(request):
    drafts = RentalProperties.objects.filter(form_status='Incomplete', is_deleted='0')
    return render(request, 'home/draft_property_list.html', {'drafts': drafts})


#Manager recipts code

    

@login_required
def management_receipts_manager(request):
    return render(request, 'home/manager.html')

def edit_management_receipt(request, pk):
    receipt = get_object_or_404(ManagementReceipts, pk=pk)
    return render(request, 'home/Manager_Edit.html', {'receipt': receipt})

class ManagementReceiptsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ManagementReceiptsFilterSerializer
    queryset = ManagementReceipts.objects.all()

    #@action(detail=False, methods=['post'], url_path='managerdatatablefilter')
    # def managerdatatablefilter(self, request):
    #     serializer = ManagementReceiptsFilterSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     data = serializer.validated_data

    #     queryset = ManagementReceipts.objects.all()

    #     # Apply filters
    #     if data.get('receipt_number'):
    #         queryset = queryset.filter(receipt_number__icontains=data['receipt_number'])
    #     if data.get('status'):
    #         queryset = queryset.filter(status=data['status'])
    #     if data.get('payment_type'):
    #         queryset = queryset.filter(payment_type=data['payment_type'])
    #     if data.get('deal_type'):
    #         queryset = queryset.filter(deal_type=data['deal_type'])
    #     if data.get('from'):
    #         try:
    #             from_date = datetime.strptime(data['from'], '%d-%m-%Y').date()
    #             queryset = queryset.filter(date__gte=from_date)
    #         except ValueError:
    #             pass
    #     if data.get('to'):
    #         try:
    #             to_date = datetime.strptime(data['to'], '%d-%m-%Y').date()
    #             queryset = queryset.filter(date__lte=to_date)
    #         except ValueError:
    #             pass
    #     if data.get('agent_name'):
    #         queryset = queryset.filter(agent_name__icontains=data['agent_name'])
    #     if data.get('unit_number'):
    #         queryset = queryset.filter(unit_number__icontains=data['unit_number'])
    #     if data.get('building_name'):
    #         queryset = queryset.filter(building_name__icontains=data['building_name'])

    #     # Pagination
    #     start = int(data.get("start", 0))
    #     length = int(data.get("length", 10))
    #     draw = int(request.data.get("draw", 1))
    #     paginated = queryset[start:start + length]

    #     # Serialize the paginated data
    #     serializer = ManagementReceiptsSerializer(paginated, many=True, context={"request": request})
    #     response_data = {
    #         "draw": int(data.get("draw", 0)),
    #         "recordsTotal": ManagementReceipts.objects.count(),
    #         "recordsFiltered": queryset.count(),
    #         "data": serializer.data,
    #         "input": data
    #     }
    #     return Response(response_data)


    # class ManagementReceiptsViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]
    # serializer_class = ManagementReceiptsFilterSerializer
    # queryset = ManagementReceipts.objects.all()

    # @action(detail=False, methods=['post'], url_path='managerdatatablefilter')
    # def managerdatatablefilter(self, request):
    #     print("📥 Raw Request Data:", request.data)

    #     serializer = ManagementReceiptsFilterSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     data = serializer.validated_data
    #     print("✅ Validated Filter Data:", data)

    #     queryset = ManagementReceipts.objects.all()
    #     print(f"🗃 Initial QuerySet Count: {queryset.count()}")

    #     # 🔍 Global Search
    #     #search_term = data.get("search", {}).get("value") or ''
    #     search_term = request.data.get("search[value]", "").strip()

    #     if search_term:
    #         print(f"🔎 Performing Global Search with term: '{search_term}'")
    #         queryset = queryset.filter(
    #             Q(receipt_number__icontains=search_term) |
    #             Q(agent_name__icontains=search_term) |
    #             Q(building_name__icontains=search_term) |
    #             Q(unit_number__icontains=search_term) |
    #             Q(project_name__icontains=search_term) |
    #             Q(received_from__icontains=search_term)
    #         )
    #         print(f"🔢 QuerySet Count after global search: {queryset.count()}")

    #     # 🧪 Field-specific filtering
    #     filter_fields = [
    #         "receipt_number", "status", "payment_type", "deal_type",
    #         "agent_name", "unit_number", "building_name"
    #     ]
    #     for field in filter_fields:
    #         value = data.get(field)
    #         if value:
    #             print(f"🔧 Applying filter -> {field}: {value}")
    #             filter_kwargs = {f"{field}__icontains": value}
    #             queryset = queryset.filter(**filter_kwargs)
    #             print(f"   🔢 Count after {field} filter: {queryset.count()}")

    #     # 📊 Pagination
    #     start = int(data.get("start", 0))
    #     length = int(data.get("length", 10))
    #     print(f"📌 Pagination - Start: {start}, Length: {length}")
    #     paginated = queryset[start:start + length]
    #     print(f"📄 Paginated Records Count: {paginated.count()}")

    #     # 🧾 Serialization
    #     response_serializer = ManagementReceiptsSerializer(paginated, many=True, context={"request": request})
    #     print("✅ Serialization Complete")
    #     print("Serializer data:",response_serializer.data)
    #     draw = int(request.data.get("draw", 1))  # Ensure it's a valid int
    #     print("🧮 Draw from request:", draw)

    #     response_data = {
    #         # "draw": int(data.get("draw", 0)),
    #         "draw": draw,
    #         "recordsTotal": queryset.count(),
    #         "recordsFiltered": queryset.count(),
    #         "data": response_serializer.data,
    #         "input": request.data
    #     }

    #     print("📤 Returning Response to DataTable")
    #     return Response(response_data, status=status.HTTP_200_OK)
    @action(detail=False, methods=['post'], url_path='managerdatatablefilter')
    def managerdatatablefilter(self, request):
        print("📥 Raw Request Data:", request.data)

        serializer = ManagementReceiptsFilterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        print("✅ Validated Filter Data:", data)

        queryset = ManagementReceipts.objects.all()
        print(f"🗃 Initial QuerySet Count: {queryset.count()}")

        # 🔍 Global Search
        search_term = request.data.get("search[value]", "").strip()
        if search_term:
            print(f"🔎 Performing Global Search with term: '{search_term}'")
            queryset = queryset.filter(
                Q(receipt_number__icontains=search_term) |
                Q(agent_name__icontains=search_term) |
                Q(building_name__icontains=search_term) |
                Q(unit_number__icontains=search_term) |
                Q(project_name__icontains=search_term) |
                Q(received_from__icontains=search_term)
            )
            print(f"🔢 QuerySet Count after global search: {queryset.count()}")

        # 🧪 Field-specific filtering
        filter_fields = [
            "receipt_number", "status", "payment_type", "deal_type",
            "agent_name", "unit_number", "building_name"
        ]
        for field in filter_fields:
            value = data.get(field)
            if value:
                print(f"🔧 Applying filter -> {field}: {value}")
                filter_kwargs = {f"{field}__icontains": value}
                queryset = queryset.filter(**filter_kwargs)
                print(f"   🔢 Count after {field} filter: {queryset.count()}")

        # 📊 Ordering
        order_column = request.data.get('order[0][column]', 1)  # Default to 1 (receipt_number)
        order_dir = request.data.get('order[0][dir]', 'asc')    # Default to asc
        print(f"🔄 Ordering - Column: {order_column}, Direction: {order_dir}")

        # Map column index to field name (adjust based on your columns array)
        columns = [
            None,  # 0: Actions column (not orderable)
            'receipt_number',  # 1
            'date',  # 2
            'cheque_no',  # 3
            'dhs',  # 4
            'fils',  # 5
            'payment_type',  # 6
            'sec_date',  # 7
            'deal_type',  # 8
            'agent_name',  # 9
            'deal_refer_no',  # 10
            'project_name',  # 11
            'building_name',  # 12
            'unit_number',  # 13
            'status',  # 14
            'received_from'  # 15
        ]
        order_field = columns[int(order_column)] if int(order_column) < len(columns) else 'receipt_number'
        order_by = f'-{order_field}' if order_dir == 'desc' else order_field
        queryset = queryset.order_by(order_by)
        print(f"🔢 QuerySet Count after ordering: {queryset.count()}")

        # 📊 Pagination
        start = int(data.get("start", 0))
        length = int(data.get("length", 10))
        print(f"📌 Pagination - Start: {start}, Length: {length}")
        paginated = queryset[start:start + length]
        print(f"📄 Paginated Records Count: {paginated.count()}")

        # 🧾 Serialization
        response_serializer = ManagementReceiptsSerializer(paginated, many=True, context={"request": request})
        print("✅ Serialization Complete")
        print("Serializer data:", response_serializer.data)
        draw = int(request.data.get("draw", 1))  # Ensure it's a valid int
        print("🧮 Draw from request:", draw)

        response_data = {
            "draw": draw,
            "recordsTotal": ManagementReceipts.objects.count(),  # Total unfiltered records
            "recordsFiltered": queryset.count(),  # Total filtered records
            "data": response_serializer.data,
            "input": request.data
        }

        print("📤 Returning Response to DataTable")
        return Response(response_data, status=status.HTTP_200_OK)
    
    # @action(detail=True, methods=['get'], url_path='downloadReceiptPDF')
    # def download_receipt(self, request, pk=None):
    #     receipt = get_object_or_404(ManagementReceipts, pk=pk)

    #     # Example: Replace this with your actual logic for file path or URL
    #     # For now, let's assume the file URL is stored in some field, e.g. receipt_file_url
    #     file_url = getattr(receipt, 'receipt_file_url', None)
    #     if not file_url:
    #         raise Http404("No file available for this receipt")

    #     if file_url.startswith('http://') or file_url.startswith('https://'):
    #         return HttpResponseRedirect(file_url)

    #     # If local file path
    #     if os.path.exists(file_url):
    #         with open(file_url, 'rb') as f:
    #             response = HttpResponse(f.read(), content_type='application/pdf')
    #             filename = os.path.basename(file_url)
    #             response['Content-Disposition'] = f'attachment; filename="{filename}"'
    #             return response

    #     raise Http404("File not found")
    @action(detail=True, methods=['get'], url_path='downloadReceiptPDF')
    def download_receipt(self, request, pk=None):
        receipt = get_object_or_404(ManagementReceipts, pk=pk)
        receipt_data = ManagementReceiptsSerializer(receipt, context={'request': request}).data
        print(receipt_data, "this is receipt PDF")

        # Render HTML template to string
        html_string = render_to_string('home/receipt_pdf_template.html', {'receipt': receipt_data})

        # Convert HTML to PDF
        html = HTML(string=html_string, base_url=request.build_absolute_uri('/'))
        pdf_file = html.write_pdf()

        # Decide if it's download or inline view
        download = request.GET.get("download") == "1"
        disposition = 'attachment' if download else 'inline'

        # Return PDF response
        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = f'{disposition}; filename="receipt_{receipt.receipt_number}.pdf"'
        return response
    @action(detail=True, methods=['get'], url_path='view-receipt')
    def view_receipt(self, request, pk=None):
        receipt = get_object_or_404(ManagementReceipts, pk=pk)
        return render(request, 'home/Manager_view.html', {'receipt': receipt})
    
    def edit_management(request, pk):
        receipt = get_object_or_404(ManagementReceipts, pk=pk)
        return render(request, 'home/Manager_Edit.html', {'receipt': receipt})
    
    

    def edit_management(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        try:
            receipt = self.get_object()
        except ManagementReceipts.DoesNotExist:
            return Response({"error": "Receipt not found"}, status=404)

        serializer = ManagementReceiptsSerializer(receipt)
        return Response(serializer.data)
    def update(self, request, pk=None):
        receipt = get_object_or_404(ManagementReceipts, pk=pk)
        serializer = ManagementReceiptsSerializer(receipt, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True, 'message': 'Receipt updated successfully.'})
        return Response(serializer.errors, status=400)
    
    @action(detail=False, methods=['get'], url_path='create-form')
    def create_form(self, request):
        # Generate the next receipt number
        last_receipt = ManagementReceipts.objects.order_by('-receipt_number').first()
        next_receipt_number = int(last_receipt.receipt_number) + 1 if last_receipt else 1000
        return render(request, 'home/Manager_Create.html', {'next_receipt_number': next_receipt_number})

    @action(detail=False, methods=['post'], url_path='create')
    def create_receipt(self, request):
        serializer = ManagementReceiptsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'message': 'Receipt created successfully.'
            }, status=status.HTTP_201_CREATED)
        return Response({
            'success': False,
            'message': 'Failed to create receipt.',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    @action(detail=True, methods=['get', 'PUT'], url_path='edit')
    def edit_receipt(self, request, pk=None):
        print("==== START edit_receipt ====")
        print(f"Received {request.method} request at /management-receipts/{pk}/edit/")

        # 1. Try to fetch the receipt
        try:
            print(f"Attempting to fetch ManagementReceipts object with pk={pk}")
            receipt = get_object_or_404(ManagementReceipts, pk=pk)
            print(f"Successfully retrieved receipt: {receipt}")
        except Http404:
            print(f"ERROR: Receipt with pk={pk} not found")
            return Response({'status': 'error', 'errors': {'detail': 'Receipt not found'}}, status=status.HTTP_404_NOT_FOUND)

        # 2. Handle GET Request — Load Edit Form
        if request.method == 'GET':
            print(f"Handling GET request: preparing form for receipt pk={pk}")
            serializer = ManagementReceiptsSerializer(receipt, context={'request': request})
            print(f"Serialized data to pre-fill form: {serializer.data}")
            print("==== END edit_receipt GET ====")
            return render(request, 'home/Manager_Edit.html', {'receipt': serializer.data})

        # 3. Handle POST Request — Save Edited Data
        elif request.method == 'POST':
            print("Handling POST request — attempt to save form data")
            print("Incoming form data:")
            for key, value in request.data.items():
                print(f"  {key} = {value}")

            serializer = ManagementReceiptsSerializer(receipt, data=request.data, partial=True)

            if serializer.is_valid():
                print("Serializer validation PASSED. Saving data...")
                serializer.save()
                print(f"Receipt with pk={pk} updated successfully")
                print(f"Updated data: {serializer.data}")
                print("==== END edit_receipt POST — SUCCESS ====")
                return Response({'status': 'success', 'data': serializer.data}, status=status.HTTP_200_OK)
            else:
                print("Serializer validation FAILED:")
                for field, error_list in serializer.errors.items():
                    print(f"  {field}: {error_list}")
                print("==== END edit_receipt POST — ERROR ====")
                return Response({'status': 'error', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
 