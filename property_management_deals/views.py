
import os
import warnings
warnings.filterwarnings("ignore")
import datetime
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from django.db.models import IntegerField
from django.db.models.functions import Cast


# Create your views here.
from django.contrib.auth import authenticate, login
# from .forms import LoginForm

from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from core.models import RentalProperties,Account as Accounts
from .serializers import AgentDropdownSerializer, DealSerializer,filterSerializer

from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
# from .forms import LoginForm, SignUpForm  # Add this import for LoginForm and SignUpForm
   

from django_filters import rest_framework as filters
from django.template import loader
from django import template
from django.urls import reverse


from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
# --- this goes outside the ViewSet class ---

from django.shortcuts import render, get_object_or_404, redirect
from .forms import PropertyForm
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
from datetime import datetime, date
from dateutil.parser import parse
from django.db import transaction
from django.contrib.auth.decorators import permission_required
from core.models import Users
from django.db import transaction, IntegrityError
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import PropertySerializer
import re
import time
from datetime import datetime
import json





# def dashboard_view(request):
#     if not request.user.is_authenticated:
#         return redirect('%s?next=%s' % ('/login/', request.path))
#     print("User authenticated:", request.user.is_authenticated)
#     print("User:", request.user)
#     print("Is anonymous:", request.user.is_anonymous)
#     return render(request, 'home/index.html')


# class UsersViewSet(viewsets.ModelViewSet):
#     queryset = Users.objects.all()
#     serializer_class = UsersSerializer

#     def update(self, request, *args, **kwargs):
#         print("DEBUG is_deleted:", request.data.get("is_deleted"))
#         return super().update(request, *args, **kwargs)
    

class PropertyAPIView(APIView):
    def get(self, request, pk):
        print("Hi")
        property_obj = get_object_or_404(RentalProperties, pk=pk)
        serializer = PropertySerializer(property_obj)
        print(serializer.data ," this is fro th getedit")
        return Response(serializer.data)

 
    
    

    def put(self, request, pk):
        print("DEBUG: PUT method triggered")
        property_obj = get_object_or_404(RentalProperties, pk=pk)
        mutable_data = {
            key: request.data.getlist(key) if len(request.data.getlist(key)) > 1 else request.data.get(key)
            for key in request.data
        }
        mutable_data.update(request.FILES)
 
        updated_files = {}
        reference_number = mutable_data.get('reference_number') or property_obj.reference_number
        is_property_aml = mutable_data.get('is_property_aml') or property_obj.is_property_aml
       
        path = f"/rental/referencenumber_CP/{reference_number}"
        is_property_aml = mutable_data.get('is_property_aml')
        if not is_property_aml:
            is_property_aml = property_obj.is_property_aml
 
        print("Is Property AML:", is_property_aml)
        property_obj.is_property_aml = is_property_aml
        property_obj.save()
        mutable_data['is_property_aml'] = is_property_aml
        mutable_data['receipt_no'] = mutable_data.get('receipt_no') or property_obj.receipt_no
 
        print(f"Mutable Data: {mutable_data}")
 
        print(f"Is Property aml: {is_property_aml}")
 
        print(f"🔍 STARTING UPDATE for Property ID: {pk}")
        print(f"📁 Reference Path: {path}")
        print(f"📥 FILE KEYS: {list(request.FILES.keys())}")
        print(f"📝 FORM DATA: {dict(request.data)}")
 
        file_fields = [
            'pms_contract', 'owner_passport_copy', 'pms_cheque_copy',
            'title_deed', 'kyc_form', 'screening',
            'poa_pp', 'poa_copy', 'owner_eid_copy', 'key_hand_over_form'
        ]
        required_file_fields = [
            'pms_contract', 'owner_passport_copy', 'pms_cheque_copy',
            'title_deed', 'kyc_form', 'screening'
        ]
 
        # Upload new files
        if request.FILES:
            for key in request.FILES.keys():
                base_field_name = key.rstrip("[]")
                if base_field_name not in file_fields:
                    print(f"⚠️ Skipping invalid file field: {base_field_name}")
                    continue
 
                files = request.FILES.getlist(key)
                for file in files:
                    timestamp = int(time.time())
                    cleaned_name = re.sub(r"[,]+", " ", file.name)
                    filename = f"{base_field_name}{timestamp}_{cleaned_name}"
                    filepath = f"{path}/{filename}"
                    print(f"⬆️ Uploading file: {filename} to {filepath}")
                    is_uploaded = upload_file_to_full_s3_url(file, filepath)  # Assuming this function exists
                    if is_uploaded:
                        updated_files.setdefault(base_field_name, []).append(filepath)
                        print(f"✅ Uploaded: {filename}")
                    else:
                        print(f"❌ Upload failed: {filename}")
                        return Response(
                            {"error": f"Failed to upload file: {filename}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR
                        )
 
        # Merge old + new files and only remove explicitly specified ones
        for field in file_fields:
            # removed_files = [f.strip() for f in mutable_data.get(f"{field}_removed", "").split(",") if f.strip()]
            removed_files = [f.strip() for f in mutable_data.get(f"{field}_mou_removed", "").split(",") if f.strip()]
 
            existing_value = getattr(property_obj, field, "") or ""
            existing_files = [f.strip() for f in existing_value.split(",") if f.strip()]
 
            # Remove explicitly marked files
            existing_files = [f for f in existing_files if f not in removed_files]
 
            new_files = updated_files.get(field, [])
            combined_files = existing_files + new_files
 
            mutable_data[field] = ",".join(combined_files)
            print(f"🔄 {field} Combined Files after removal: {mutable_data[field]}")
        # Validate required file fields
        for field in required_file_fields:
            val = mutable_data.get(field, "") or getattr(property_obj, field, "")
            if not val:
                print(f"❌ Validation failed: {field} is required")
                return Response({"error": f"{field} is required."}, status=status.HTTP_400_BAD_REQUEST)
 
        # Handle date fields (including cheque_date)
        date_fields = [
            'deal_date',
            'pm_start_date',
            'pm_end_date',
            'tenancy_start_date',
            'tenancy_end_date',
            #'cheque_date'
        ]
 
        accepted_formats = ["%Y-%m-%d", "%d-%m-%Y", "%d-%m-%y"]
 
        for field in date_fields:
            if field in mutable_data:
                value = mutable_data[field]
                print(f"\n🔍 Processing field: {field} -> {value}")
 
                if isinstance(value, list):
                    formatted_list = []
                    for date_str in value:
                        print(f"   ⏳ Parsing list item: {date_str}")
                        if isinstance(date_str, str) and date_str.strip() and date_str != '0':
                            for fmt in accepted_formats:
                                try:
                                    parsed_date = datetime.strptime(date_str, fmt)
                                    formatted_str = parsed_date.strftime("%d-%m-%Y")
                                    formatted_list.append(formatted_str)
                                    print(f"   ✅ Parsed: {date_str} -> {formatted_str}")
                                    break
                                except ValueError:
                                    continue
                            else:
                                print(f"   ❌ Failed to parse date: {date_str}")
                        else:
                            print(f"   ❌ Non-string, empty, or invalid in list: {date_str}")
                    mutable_data[field] = formatted_list
                    print(f"   🔄 Final list for {field}: {mutable_data[field]}")
 
                elif isinstance(value, str) and value.strip() and value != '0':
                    print(f"   ⏳ Parsing single string date: {value}")
                    for fmt in accepted_formats:
                        try:
                            parsed_date = datetime.strptime(value, fmt)
                            formatted_str = parsed_date.strftime("%d-%m-%Y")
                            mutable_data[field] = formatted_str
                            print(f"   ✅ Parsed: {value} -> {formatted_str}")
                            break
                        except ValueError:
                            continue
                    else:
                        print(f"   ❌ Failed to parse string date: {value}")
 
         # ====== CHEQUE DATE HANDLING ======
        cheque_date_value = mutable_data.get('cheque_date')
 
        if cheque_date_value:
            if isinstance(cheque_date_value, str):
                try:
                    parsed_cheque_dates = json.loads(cheque_date_value)
                except json.JSONDecodeError:
                    parsed_cheque_dates = [cheque_date_value]
            elif isinstance(cheque_date_value, list):
                parsed_cheque_dates = cheque_date_value
            else:
                parsed_cheque_dates = []
 
            formatted_cheques = []
            accepted_formats = ["%Y-%m-%d", "%d-%m-%Y", "%d-%m-%y"]
            for date_str in parsed_cheque_dates:
                if date_str and date_str.strip() and date_str != '0':
                    for fmt in accepted_formats:
                        try:
                            parsed_date = datetime.strptime(date_str.strip(), fmt)
                            formatted_cheques.append(parsed_date.strftime("%d-%m-%Y"))
                            break
                        except ValueError:
                            continue
 
            mutable_data['cheque_date'] = " ".join(formatted_cheques)
            print("✅ Final formatted cheque_date (update):", mutable_data['cheque_date'])
        # ====== END CHEQUE DATE HANDLING ======
 
        # Clean other fields (handle lists from request.POST)
        for key in list(mutable_data.keys()):
            if key != 'cheque_date' and isinstance(mutable_data[key], list):
                mutable_data[key] = mutable_data[key][0] if mutable_data[key] else ''

        if property_obj.form_status == "Incomplete":
            mutable_data['submitted_date'] = timezone.now().date()
 
        mutable_data['form_status'] = 'Complete'
 
        if request.data.get('receipt_no'):
            ManagementReceipts.objects.filter(receipt_number=request.data.get('receipt_no')).update(status='Used',deal_refer_no=request.data.get('reference_number'))
 
        if mutable_data.get("is_approved_rejected") and mutable_data.get("is_approved_rejected") in ["A", "R", "F"]:
                mutable_data['approved_rejected_by'] = request.user.email
        # Apply updates
        serializer = PropertySerializer(property_obj, data=mutable_data, partial=True)
        if serializer.is_valid():
            serializer.save()
            # Save file fields explicitly again if needed
            for field in file_fields:
                setattr(property_obj, field, mutable_data.get(field, ""))
            property_obj.save()
 
            # Refresh serialized data
            serializer = PropertySerializer(property_obj)
            print(f"✅ Saved instance put: {serializer.data}")
            return Response(serializer.data)
 
        print(f"❌ Serializer errors: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
   


def edit_property_page(request, pk):
    print("🔍 Called edit_property_page")
    property_obj = get_object_or_404(RentalProperties, pk=pk)

    agents_raw = Users.objects.all()
 
    # Filter out users with blank/null/whitespace-only names
    agents = [agent for agent in agents_raw if agent.name and agent.name.strip()]

    print("---- Cleaned Agent Names ----")
    for agent in agents:
        print(agent.name.strip())
    print("-----------------------------")
    

    if request.method == "POST":
        form = PropertyForm(request.POST, request.FILES, instance=property_obj)
        if form.is_valid():
            form.save()
            return redirect('rental-property-list')

    form = PropertyForm(instance=property_obj)

    # ✅ Fetch unique, cleaned receipt numbers
    receipt_nos_raw = RentalProperties.objects.values_list('receipt_no', flat=True).distinct()
    receipt_nos = [rcpt.strip() for rcpt in receipt_nos_raw if rcpt and rcpt.strip()]

    return render(request, 'home/edit_property.html', {
        'form': form,
        'property': property_obj,
        'receipt_nos': receipt_nos,
        'agents': agents,   # ✅ Pass to template
    })




def download_receipt(request, pk):
    property = get_object_or_404(RentalProperties, pk=pk)
    if property.receipt_file:  # Assuming you have a FileField for receipts
        file_path = property.receipt_file.path
        if os.path.exists(file_path):
            return FileResponse(open(file_path, 'rb'), content_type='application/pdf')
    # Fallback if no file exists
    return HttpResponse("Receipt not found", status=404)





@csrf_exempt
def rental_property_create(request):
    print("DEBUG: Entering rental_property_create")  # Log entry to function
    print("DEBUG: Request method:", request.method)  # Log request method
    print("DEBUG: POST data:", request.POST)  # Log all POST data
    print("DEBUG: FILES:", request.FILES)  # Log uploaded files

    if request.method == 'POST':
        is_draft = request.path == '/save-draft/' or 'save_draft' in request.POST
        is_create = 'create_property' in request.POST
        print("DEBUG: is_draft:", is_draft, "is_create:", is_create)  # Log submission type

        # Get the account_id
        # account_id = request.POST.get('account_id') or (
        #     request.user.account_id 
        #     if request.user.is_authenticated and hasattr(request.user, 'account_id') and request.user.account_id 
        #     else None
        # )

        account_id = (
            request.user.account_id 
            if request.user.is_authenticated and hasattr(request.user, 'account_id') and request.user.account_id 
            else None
        )
        print("DEBUG: account_id:", account_id)  # Log account_id value

        # Validate account_id
        if not account_id or not Accounts.objects.filter(id=account_id).exists():
            print("DEBUG: Invalid or missing account_id, returning 400")
            return HttpResponse("Invalid or missing account ID", status=400)

        # Custom multi-file upload
        reference_number = request.POST.get('reference_number') or f"AUTO{account_id}_{int(time.time())}"
        s3_path = f"rental/referencenumber_CP/{reference_number}"

        uploaded_files = {}
        file_fields = [
            'pms_contract', 'title_deed', 'poa_copy', 'kyc_form',
            'owner_passport_copy', 'pms_cheque_copy', 'poa_pp',
            'key_hand_over_form', 'screening'
        ]

        # Process file uploads
        for field in file_fields:
            uploaded_files[field] = ""
            files = request.FILES.getlist(field)
            saved_filenames = []
            for file in files:
                timestamp = int(time.time())
                cleaned_name = re.sub(r"[,]+", " ", file.name)
                filename = f"{field}{timestamp}_{cleaned_name}"
                full_path = f"{s3_path}/{filename}"
                is_uploaded = upload_file_to_full_s3_url(file, full_path)
                if is_uploaded:
                    saved_filenames.append(filename)
            uploaded_files[field] = ",".join(saved_filenames)

        # Auto-increment deal_sno for the specific account_id
        with transaction.atomic():
            last_sno = RentalProperties.objects.filter(account_id=account_id).select_for_update().aggregate(Max('deal_sno'))['deal_sno__max'] or 0
            new_sno = last_sno + 1
            print("DEBUG: last_sno:", last_sno)  # Log last_sno
            print("DEBUG: new_sno:", new_sno)  # Log new_sno

            is_entered_value = request.POST.get('is_entered_in_finance_system') or '0'

            try:
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
                    account_id=account_id,  # Set the account_id
                    form_status='Incomplete' if is_draft else 'Complete',
                    status='Active',
                    is_deleted='N',
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
                print("DEBUG: Created rental with deal_sno:", rental.deal_sno, "account_id:", rental.account_id)  # Log created record
            except Exception as e:
                print("DEBUG: Error creating rental:", str(e))
                return HttpResponse(f"Error creating rental: {str(e)}", status=500)

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
    print("🧠 Rental_PropertyViewSet is loaded at startup")
    queryset = RentalProperties.objects.all()
    serializer_class = filterSerializer  # for default `list`, `retrieve`
    # pagination_class = CustomPagination  # Custom pagination class

    permission_classes = [permissions.IsAuthenticated]

 

    def update(self, request, *args, **kwargs):
        print("DEBUG is_deleted:", request.data.get("is_deleted"))  # Add this
        return super().update(request, *args, **kwargs)

    
    def get_serializer_class(self):
        if self.action in ['create', 'edit', 'custom_update']:
            return PropertySerializer
        return filterSerializer
    

    def list(self, request, *args, **kwargs):
        print("🔥 Rental_PropertyViewSet.list() called")
        queryset = self.get_queryset()
        
        # Update status for each object in the queryset
        for obj in queryset:
            obj.update_status_if_needed()  # Call model method

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.update_status_if_needed()  # Call model method
        return super().retrieve(request, *args, **kwargs)

   
    
    @action(detail=False, methods=['get'], url_path='create-form')
    def create_form(self, request):
        
        from core.models import Users
        form = PropertyForm()

        agents_raw = Users.objects.filter(account = request.user.account_id)

        # Filter out users with blank/null/whitespace-only names
        agents = [agent for agent in agents_raw if agent.name and agent.name.strip()]

        print("---- Cleaned Agent Names ----")
        for agent in agents:
            print(agent.name.strip())
        print("-----------------------------")

        # Fetch unique, non-empty receipt numbers
        receipt_no = ManagementReceipts.objects.filter(account_id = request.user.account_id)
       

        print("----- Valid Receipt Numbers -----")
        for rcpt in receipt_no:
            print(rcpt)
        print("----------------------------------")



        return render(request, 'home/create_property.html', {'form': form, 'agents': agents, 'receipt_nos': receipt_no})


    
    @action(detail=False, methods=['post'], url_path='create')
    def create(self, request):
        print("🚨 CUSTOM CREATE METHOD CALLED")
        print("Request data:", dict(request.data))
        print("File keys:", list(request.FILES.keys()))
 
        # Get and validate account_id
        account_id = (
            request.user.account.id
            if request.user.is_authenticated and hasattr(request.user, 'account') and request.user.account
            else None
        )
        print("DEBUG: account_id extracted:", account_id)
        print("DEBUG: request.user.account (raw):", getattr(request.user, 'account', 'NOT SET'))
        print("DEBUG: User is_authenticated:", request.user.is_authenticated)
 
        if not account_id:
            print("DEBUG: account_id is None or empty — EXITING EARLY")
            return Response(
                {'success': False, 'message': 'Account ID is required and cannot be empty'},
                status=status.HTTP_400_BAD_REQUEST
            )
 
        # Validate account_id exists in Accounts
        if not Accounts.objects.filter(id=account_id).exists():
            print("DEBUG: Invalid account_id — EXITING EARLY:", account_id)
            return Response(
                {'success': False, 'message': f'Account ID {account_id} does not exist'},
                status=status.HTTP_400_BAD_REQUEST
            )
        print("DEBUG: account_id validated OK:", account_id)
 
        # Auto-increment deal_sno for the specific account_id
        with transaction.atomic():
            queryset = RentalProperties.objects.filter(account_id=account_id).select_for_update()
            last_sno = queryset.aggregate(Max('deal_sno'))['deal_sno__max'] or 0
            new_sno = last_sno + 1
            print("DEBUG: last_sno:", last_sno, "new_sno:", new_sno)
 
            # Initialize data dictionary
            data = {}
            updated_files = {}
 
            # Define file fields
            file_fields = [
                'pms_contract', 'owner_passport_copy', 'owner_eid_copy',
                'pms_cheque_copy', 'title_deed', 'poa_pp', 'poa_copy',
                'key_hand_over_form', 'kyc_form', 'screening'
            ]
 
            # Generate reference_number
            reference_number = request.data.get('reference_number', f"AUTO{account_id}_{int(time.time())}")
            data['reference_number'] = reference_number
            path = f"/rental/referencenumber_CP/{reference_number}"
            print(f"📁 Reference Path: {path}")
 
            # --- DUPLICATE CHECK ---
            if RentalProperties.objects.filter(reference_number=reference_number).exists():
                print("DEBUG: Duplicate reference_number — EXITING EARLY:", reference_number)
                return Response(
                    {'success': False, 'message': f'Reference Number "{reference_number}" already exists.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
 
           
 
            # Handle draft submission
            if request.data.get('save_as') == 'draft':
                print("DEBUG: Entering DRAFT submission block")
                required_fields = [
                    'submitted_by_agent', 'deal_date', 'reference_number', 'project_name', 'building_name',
                    'unit_details', 'pms_price', 'pm_start_date', 'pm_end_date', 'tenancy_start_date',
                    'tenancy_end_date', 'owner_first_name', 'owner_source', 'owner_mobile', 'owner_email',
                    'seller_nationality'
                ]
                for field in required_fields:
                    if field not in request.data or not request.data[field]:
                        print("DEBUG: Missing required field for draft:", field)
                        return Response(
                            {'success': False, 'message': f'{field} is required for draft.'},
                            status=status.HTTP_400_BAD_REQUEST
                        )
 
                draft_data = {
                    field: request.data[field] for field in required_fields if field != 'submitted_by_agent' and field in request.data
                }
                draft_data.update({
                    'form_status': 'Incomplete',
                    'is_approved_rejected': request.data.get('is_approved_rejected', 'P'),
                    'is_entered_in_finance_system': '0',
                    'is_deleted': request.data.get('is_deleted', 'N'),
                    'status': 'Inactive',
                    'account_id': account_id,
                    #'account': account_id,
                    'deal_sno': new_sno,
                    'submitted_by_user_id': request.data.get('submitted_by_agent') or (
                        request.user.id if request.user.is_authenticated else 0
                    ),
                    'submitted_date': timezone.now().date(),
                    'created_at': timezone.now(),
                    'updated_at': timezone.now(),
                    'is_property_aml': request.data.get('is_property_aml', 'No'),
                    'screening_comments': request.data.get('screening_comments', ''),
                    'seller_nationality': request.data.get('seller_nationality', ''),
                    'buyer_nationality': request.data.get('buyer_nationality', ''),
                    'no_of_cheque': request.data.get('no_of_cheque', ''),
                    'receipt_no': request.data.get('receipt_no'),
                    #Remaining fields
                    'agency_name': request.data.get('agency_name', ''),
                    'agent_name': request.data.get('agent_name', ''),
                    'brn': request.data.get('brn', ''),
                    'agent_phone': request.data.get('agent_phone', ''),
                    'agent_email': request.data.get('agent_email', ''),
                    'total_commission': request.data.get('total_commission', ''),
                    'less_outside_commission': request.data.get('less_outside_commission', ''),
                    'net_commission': request.data.get('net_commission', ''),
                    'classic': request.data.get('classic', ''),
                    'agent1': request.data.get('agent1', ''),
                    'agent_name1': request.data.get('agent_name1', ''),
                    'agent2': request.data.get('agent2', ''),
                    'agent_name2': request.data.get('agent_name2', ''),
                    'agent3': request.data.get('agent3', ''),
                    'agent_name3': request.data.get('agent_name3', ''),
                    'agent_comment': request.data.get('agent_comment', ''),
                    'kyc_number': request.data.get('kyc_number', ''),
                    'comments': request.data.get('comments',''),
                    'screening_comments':request.data.get('screening_comments',''),
 
                })
                print("DEBUG: Draft data — account_id:", draft_data.get('account_id'))
 
                # Format date fields
                draft_date_fields = ['deal_date', 'pm_start_date', 'pm_end_date', 'tenancy_start_date', 'tenancy_end_date']
                for field in draft_date_fields:
                    if field in draft_data and draft_data[field]:
                        for fmt in ["%Y-%m-%d", "%d-%m-%Y", "%d-%m-%y"]:
                            try:
                                parsed = datetime.strptime(draft_data[field], fmt)
                                draft_data[field] = parsed.strftime("%d-%m-%Y")
                                print(f"DEBUG: Draft formatted {field}: {draft_data[field]}")
                                break
                            except ValueError:
                                continue
                        else:
                            print(f"DEBUG: Invalid date format for draft {field}: {draft_data[field]}")
                            return Response(
                                {'success': False, 'message': f'Invalid date format for {field}'},
                                status=status.HTTP_400_BAD_REQUEST
                            )
 
                # Handle cheque dates
                cheque_dates = request.POST.getlist('cheque_date[]')
                print("DEBUG: Draft received cheque_dates:", cheque_dates)
                formatted_cheque_dates = []
                accepted_formats = ["%Y-%m-%d", "%d-%m-%Y", "%d-%m-%y"]
                for date_str in cheque_dates:
                    if date_str.strip() and date_str != '0':
                        for fmt in accepted_formats:
                            try:
                                parsed_date = datetime.strptime(date_str.strip(), fmt)
                                formatted_cheque_dates.append(parsed_date.strftime("%d-%m-%Y"))
                                print(f"DEBUG: Draft formatted cheque_date: {date_str} -> {formatted_cheque_dates[-1]}")
                                break
                            except ValueError:
                                continue
                        else:
                            print(f"DEBUG: Invalid cheque date format for draft: {date_str}")
                            return Response(
                                {'success': False, 'message': f'Invalid date format for cheque date: {date_str}'},
                                status=status.HTTP_400_BAD_REQUEST
                            )
                draft_data['cheque_date'] = " ".join(formatted_cheque_dates) if formatted_cheque_dates else ''
                print("DEBUG: Draft cheque_date (joined):", draft_data['cheque_date'])
 
                # Handle file uploads for draft
                required_file_fields_draft = ['screening']
                for field in file_fields:
                    file_key = f"{field}[]"
                    if file_key in request.FILES:
                        files = request.FILES.getlist(file_key)
                        removed_files = request.data.get(f"{field}_removed", '').split(',') if request.data.get(f"{field}_removed") else []
                       
                        # Deduplicate files by name + size
                        seen = set()
                        valid_files = []
                        for f in files:
                            key = (f.name, f.size)  # Unique per file content/name
                            if key not in seen and f.name not in removed_files:
                                seen.add(key)
                                valid_files.append(f)
                       
                        file_paths = []
                        for file in valid_files:
                            timestamp = int(time.time() * 1000)  # Milliseconds for uniqueness
                            cleaned_name = re.sub(r"[,]+", " ", file.name)
                            filename = f"{field}{timestamp}_{cleaned_name}"
                            filepath = f"{path}/{filename}"
                            if upload_file_to_full_s3_url(file, filepath):  # Ensure this function is defined
                                file_paths.append(filepath)
                                print(f"✅ Uploaded draft file: {filename}")
                            else:
                                print(f"❌ Draft file upload failed: {filename}")
                                return Response(
                                    {"error": f"Failed to upload file: {filename}"},
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                                )
                        draft_data[field] = ','.join(file_paths) if file_paths else ''
                        print(f"DEBUG: Draft {field} paths:", draft_data[field])
                    else:
                        draft_data[field] = ''
 
                # Validate required file fields for draft
                for field in required_file_fields_draft:
                    if not draft_data.get(field):
                        print(f"DEBUG: Missing required draft file field: {field}")
                        return Response(
                            {'success': False, 'message': f'At least one file is required for {field}.'},
                            status=status.HTTP_400_BAD_REQUEST
                        )
 
                # Save draft
                print("DEBUG: Draft data before serializer:", draft_data)
                serializer = PropertySerializer(data=draft_data, partial=True, draft=True)
                print("DEBUG: Draft serializer fields:", list(serializer.fields.keys()))
                print("DEBUG: Is account_id in draft serializer fields?", 'account_id' in serializer.fields)
                print("DEBUG: Is account_id read-only in draft?", serializer.fields.get('account_id', {}).read_only if 'account_id' in serializer.fields else 'N/A')

                if request.data.get("is_approved_rejected") in ["A", "R", "W"]:
                    draft_data['approved_rejected_by'] = request.user.email
 
                if request.data.get('receipt_no'):
                    ManagementReceipts.objects.filter(receipt_number=request.data.get('receipt_no')).update(status='Used',deal_refer_no=request.data.get('reference_number'))
 
                if serializer.is_valid():
                    try:
                        instance = serializer.save()
                        print("DEBUG: Draft saved — instance.account_id:", getattr(instance, 'account_id', 'NOT SET'))
                        print("DEBUG: Draft saved instance data:", PropertySerializer(instance).data)
                        return Response(
                            {'success': True, 'message': 'Draft saved successfully', 'data': {'id': instance.id}},
                            status=status.HTTP_201_CREATED
                        )
                    except IntegrityError as e:
                        print("DEBUG: Draft database save failed (IntegrityError):", str(e))
                        return Response(
                            {'success': False, 'message': f'Database error saving draft: {str(e)}'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR
                        )
                    except Exception as e:
                        print("DEBUG: Draft database save failed:", str(e))
                        return Response(
                            {'success': False, 'message': f'Unexpected error saving draft: {str(e)}'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR
                        )
                print("DEBUG: Draft serializer errors:", serializer.errors)
                return Response(
                    {'success': False, 'message': serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )
 
            # Full submission
            print("DEBUG: Entering FULL submission block")
            # Copy non-file fields
            for key in request.data:
                if key not in request.FILES and not key.endswith('_removed'):
                    data[key] = request.data[key]
            print("DEBUG: After copying request.data — account_id in data?", 'account_id' in data, data.get('account_id'))
 
            # Process file uploads
            required_file_fields = ['pms_contract', 'owner_passport_copy', 'pms_cheque_copy', 'title_deed', 'kyc_form', 'screening']
            for field in file_fields:
                file_key = f"{field}[]"
                if file_key in request.FILES:
                    files = request.FILES.getlist(file_key)
                    removed_files = request.data.get(f"{field}_removed", '').split(',') if request.data.get(f"{field}_removed") else []
                    # valid_files = [f for f in files if f.name not in removed_files]
                    valid_files = list(files)
                    file_paths = []
                    for file in valid_files:
                        timestamp = int(time.time())
                        cleaned_name = re.sub(r"[,]+", " ", file.name)
                        filename = f"{field}{timestamp}_{cleaned_name}"
                        filepath = f"{path}/{filename}"
                        if upload_file_to_full_s3_url(file, filepath):
                            file_paths.append(filepath)
                            print(f"✅ Uploaded full submission file: {filename}")
                        else:
                            print(f"❌ Full submission file upload failed: {filename}")
                            return Response(
                                {"error": f"Failed to upload file: {filename}"},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR
                            )
                    updated_files[field] = file_paths
                else:
                    updated_files[field] = []
                data[field] = ','.join(updated_files[field]) if updated_files[field] else ''
                print(f"DEBUG: Full submission {field} paths:", data[field])
 
            # Validate required file fields
            for field in required_file_fields:
                if not data.get(field):
                    print(f"DEBUG: Missing required file field: {field}")
                    return Response(
                        {'success': False, 'message': f'At least one file is required for {field}.'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
 
            # Handle cheque dates
           
            cheque_dates = []
            if 'cheque_date' in request.data:
                cheque_date_data = request.data['cheque_date']
                try:
                    if isinstance(cheque_date_data, str):
                        cheque_dates = json.loads(cheque_date_data)
                    elif isinstance(cheque_date_data, list):
                        cheque_dates = cheque_date_data
                except json.JSONDecodeError:
                    cheque_dates = request.POST.getlist('cheque_date[]')
            else:
                cheque_dates = request.POST.getlist('cheque_date[]')
 
            print("DEBUG: Received cheque_dates:", cheque_dates)
 
            formatted_cheque_dates = []
            accepted_formats = ["%Y-%m-%d", "%d-%m-%Y", "%d-%m-%y"]
 
            for date_str in cheque_dates:
                if date_str and date_str.strip() and date_str != '0':
                    for fmt in accepted_formats:
                        try:
                            parsed_date = datetime.strptime(date_str.strip(), fmt)
                            formatted_cheque_dates.append(parsed_date.strftime("%d-%m-%Y"))  # <-- Use append
                            print(f"DEBUG: Formatted cheque_date: {date_str} -> {formatted_cheque_dates[-1]}")
                            break
                        except ValueError:
                            continue
                    else:
                        print(f"DEBUG: Invalid cheque date format: {date_str}")
                        return Response(
                            {'success': False, 'message': f'Invalid date format for cheque date: {date_str}'},
                            status=status.HTTP_400_BAD_REQUEST
                        )
 
            # Join with space
            data['cheque_date'] = " ".join(formatted_cheque_dates)
            print("DEBUG: Full submission cheque_dates:", data['cheque_date'])
 
 
            # Convert other date fields to dd-mm-yyyy
            date_fields = [
                'deal_date', 'pm_start_date', 'pm_end_date',
                'tenancy_start_date', 'tenancy_end_date'
            ]
            for field in date_fields:
                if field in data and data[field]:
                    for fmt in accepted_formats:
                        try:
                            parsed_date = datetime.strptime(data[field], fmt)
                            data[field] = parsed_date.strftime("%d-%m-%Y")
                            print(f"DEBUG: Formatted {field}: {data[field]}")
                            break
                        except ValueError:
                            continue
                    else:
                        print(f"DEBUG: Invalid date format for {field}: {data[field]}")
                        return Response(
                            {'success': False, 'message': f'Invalid date format for {field}'},
                            status=status.HTTP_400_BAD_REQUEST
                        )
 
            # Clean list fields
            for key in list(data.keys()):
                if key != 'cheque_date' and isinstance(data[key], list):
                    data[key] = data[key][0] if data[key] else ''
                    print(f"DEBUG: Cleaned list field {key}: {data[key]}")
 
            # Add required fields
            data.update({
                'submitted_by_user_id': request.user.id if request.user.is_authenticated else 0,
                'submitted_date': timezone.now().date(),
                'account_id': account_id,
                #'account': account_id,
                'deal_sno': new_sno,
                'form_status': 'Complete',
                'is_approved_rejected': request.data.get('is_approved_rejected', 'P'),
                'is_entered_in_finance_system': '0',
                'is_deleted': request.data.get('is_deleted', 'N'),
                'status': 'Active',
                'created_at': timezone.now(),
                'updated_at': timezone.now(),
                'is_property_aml': request.data.get('is_property_aml', 'No'),
                'screening_comments': request.data.get('screening_comments', ''),
                'seller_nationality': request.data.get('seller_nationality', ''),
                'buyer_nationality': request.data.get('buyer_nationality', '')
            })
            print("DEBUG: After data.update() — account_id:", data['account_id'])
            print("DEBUG: Full data dict preview:", {k: v for k, v in data.items()})
 
            # Update ManagementReceipts
            if 'receipt_no' in data and data['receipt_no'] and data['receipt_no'] != 'Null':
                reference_number = data.get('reference_number') or None
                try:
                    ManagementReceipts.objects.filter(receipt_number=data['receipt_no']).update(deal_refer_no=reference_number,status='Used')
                    print("DEBUG: Updated ManagementReceipts with deal_refer_no:", reference_number)
                except Exception as e:
                    print(f"DEBUG: Error updating ManagementReceipts: {str(e)}")
                    return Response(
                        {'success': False, 'message': f'Error updating receipt: {str(e)}'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
 
            # Validate and save
            print("DEBUG: Creating serializer with data...")
            serializer = PropertySerializer(data=data)
            print("DEBUG: Serializer fields:", list(serializer.fields.keys()))
            print("DEBUG: Is account_id in serializer fields?", 'account_id' in serializer.fields)
            print("DEBUG: Is account_id read-only?", serializer.fields.get('account_id', {}).read_only if 'account_id' in serializer.fields else 'N/A')
 
            # if request.data.get('receipt_no'):
            #     ManagementReceipts.objects.filter(receipt_no=request.data.get('receipt_no')).update(status='Used',deal_refer_no=request.data.get('reference_number'))
            if serializer.is_valid():
                try:
                    instance = serializer.save()
                    print("DEBUG: Full submission saved — instance.account_id:", getattr(instance, 'account_id', 'NOT SET'))
                    print("DEBUG: Full saved instance data:", PropertySerializer(instance).data)
                    return Response(
                        {'success': True, 'data': serializer.data},
                        status=status.HTTP_201_CREATED
                    )
                except IntegrityError as e:
                    print("DEBUG: Full submission database save failed (IntegrityError):", str(e))
                    return Response(
                        {'success': False, 'message': f'Database error: {str(e)}'},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )
                except Exception as e:
                    print("DEBUG: Full submission database save failed:", str(e))
                    return Response(
                        {'success': False, 'message': f'Unexpected error: {str(e)}'},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )
            print("DEBUG: Full submission serializer INVALID — NO SAVE HAPPENED")
            print("DEBUG: Full submission serializer errors:", serializer.errors)
            print("DEBUG: account_id in data during failure:", data.get('account_id'))
            return Response(
                {'success': False, 'message': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
 
    
   
    def get_queryset(self):
        print("🧠 get_queryset() called from Rental_PropertyViewSet")
        return RentalProperties.objects.filter(is_deleted='N')


    def list(self, request, *args, **kwargs):
        print("🔥 Rental_PropertyViewSet.list() called")
        queryset = self.get_queryset()
        
        for obj in queryset:
            self.update_status_if_needed(obj)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        self.update_status_if_needed(instance)
        return super().retrieve(request, *args, **kwargs)


    @action(detail=True, methods=['get'], url_path='view')
    def view_property(self, request, pk=None):

        property = get_object_or_404(RentalProperties, pk=pk)
        receipt_no = property.receipt_no
        related_receipts = None
        if receipt_no not in [None, '']:
            try:
                receipt_no = int(receipt_no)
                related_receipts = ManagementReceipts.objects.filter(receipt_number=receipt_no).first()
            except ValueError:
                pass  # or handle invalid format gracefully


        serializer = DealSerializer(property )
        return render(request, 'home/view_property.html', {'property': serializer.data ,'receipts': related_receipts})
    
    @action(detail=True, methods=['post', 'put'], url_path='update-finance')
    #@permission_required('property_management_deals.update_finance_status_properties_rentalproperties', raise_exception=True)
    def update_finance(self, request, pk=None):
        property = get_object_or_404(RentalProperties, pk=pk)
        print("🔔 Full request data:", request.data)
        print("📝 Current property.no_of_cheque:", property.no_of_cheque)
        data = request.data.copy()
        if 'no_of_cheque' not in data and property.no_of_cheque:
            data['no_of_cheque'] = property.no_of_cheque
        if 'receipt_no' not in data and property.receipt_no:
            data['receipt_no'] = property.receipt_no
    
        # Print specific fields you care about
        
        # serializer = PropertySerializer(instance=property, data=request.data, partial=True)
        serializer = PropertySerializer(instance=property, data=data, partial=True)
        
        print("🔔 Serializer input data:", serializer.initial_data)
        if serializer.is_valid():
            # Update is_entered_in_finance_system if provided
            if 'is_entered_in_finance_system' in request.data:
                property.is_entered_in_finance_system = request.data['is_entered_in_finance_system']
            
            # Update comments_finance if provided
            if 'comments_finance' in request.data:
                property.comments_finance = request.data['comments_finance']
            
            property.save()
            return Response(PropertySerializer(property).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
   
   
    @action(detail=True, methods=["post"], url_path="edit")
    def edit(self, request, pk=None):
        instance = self.get_object()
        agents_raw = Users.objects.all()
 
        # Filter out users with blank/null/whitespace-only names
        agents = [agent for agent in agents_raw if agent.name and agent.name.strip()]

        print("---- Cleaned Agent Names ----")
        for agent in agents:
            print(agent.name.strip())
        print("-----------------------------")
        serializer = self.get_serializer(instance, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST,{'agents': agents})
        return Response(
            {
                'errors': serializer.errors,
                'agents': [agent.name.strip() for agent in agents]
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        serializer = self.get_serializer(instance)
        print(serializer.data)

        return Response(serializer.data)

 
        
    def update(self, request, *args, **kwargs):
        print("check fo rthe Get api UPdate")
        property_obj = self.get_object()
        mutable_data = {key: request.data.getlist(key) if len(request.data.getlist(key)) > 1 else request.data.get(key) for key in request.data}
        mutable_data.update(request.FILES)
 
        updated_files = {}
        reference_number = mutable_data.get('reference_number') or property_obj.reference_number
        path = f"rental/referencenumber_CP/{reference_number}"
 
        print(f"🔍 STARTING UPDATE for Property ID: {kwargs.get('pk')}")
        print(f"📁 Reference Path: {path}")
        print(f"📥 FILE KEYS: {list(request.FILES.keys())}")
        print(f"📝 FORM DATA: {dict(request.data)}")
 
        file_fields = ['pms_contract', 'owner_passport_copy', 'pms_cheque_copy', 'title_deed', 'kyc_form', 'screening']
 
        # === Process file uploads ===
        if request.FILES:
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
                        updated_files.setdefault(base_field_name, []).append(filepath)
                        print(f"✅ Uploaded: {filename}")
                    else:
                        print(f"❌ Upload failed: {filename}")
                        return Response({"error": f"Failed to upload file: {filename}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 
            for field in file_fields:
                removed_files = mutable_data.get(f"{field}_removed", "").split(",")
                existing = getattr(property_obj, field, "") or ""
                existing_files = existing.split(",") if existing else []
                existing_files = [f for f in existing_files if f and f not in removed_files]
                new_files = updated_files.get(field, [])
                combined_files = existing_files + new_files
                mutable_data[field] = ",".join(combined_files) if combined_files else ""
                print(f"🔄 {field}: {mutable_data[field]}")
 
        # === Validate required file fields ===
        for field in file_fields:
            existing_value = getattr(property_obj, field, "") or ""
            new_value = mutable_data.get(field, existing_value)
            if not new_value and request.FILES.get(f"{field}[]") is None and not existing_value:
                print(f"❌ Validation failed: {field} is required")
                return Response({"error": f"{field} is required."}, status=status.HTTP_400_BAD_REQUEST)
 
        # === Format cheque_date[] list into single string ===
        cheque_dates = []
        for key in list(mutable_data.keys()):
            if key.startswith('cheque_date['):
                value = mutable_data[key]
                if value:
                    cheque_dates.append(value)
                del mutable_data[key]
        if cheque_dates:
            formatted_cheques = []
            for date_str in cheque_dates:
                for fmt in ["%Y-%m-%d", "%d-%m-%Y", "%d-%m-%y"]:
                    try:
                        parsed = datetime.strptime(date_str.strip(), fmt)
                        formatted_cheques.append(parsed.strftime("%d-%m-%Y"))
                        break
                    except ValueError:
                        continue
            mutable_data["cheque_date"] = " ".join(formatted_cheques)
            print(f"✅ Final formatted cheque_date: {mutable_data['cheque_date']}")
 
        # === Format other individual date fields ===
        date_fields = [
            'deal_date', 'pm_start_date', 'pm_end_date',
            'tenancy_start_date', 'tenancy_end_date'
        ]
        accepted_formats = ["%Y-%m-%d", "%d-%m-%Y", "%d-%m-%y"]
 
        for field in date_fields:
            if field in mutable_data and mutable_data[field]:
                original_value = mutable_data[field]
                if isinstance(original_value, list):
                    original_value = original_value[0]
                for fmt in accepted_formats:
                    try:
                        parsed_date = datetime.strptime(original_value.strip(), fmt)
                        mutable_data[field] = parsed_date.strftime("%d-%m-%Y")
                        break
                    except Exception:
                        continue
                else:
                    print(f"❌ Invalid date format for {field}: {original_value}")
                    return Response({field: [f"Invalid date format: '{original_value}'. Expected dd-mm-yyyy."]},
                                    status=status.HTTP_400_BAD_REQUEST)
 
        # === Update via serializer ===
        serializer = self.get_serializer(property_obj, data=mutable_data, partial=True)
        if serializer.is_valid():
            self.perform_update(serializer)
            print(f"✅ Saved instance edit: {serializer.data}")
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
         


    #getting data for renew
    @action(detail=True, methods=['get'], url_path='renew')
    def renew_property_page(self, request, pk=None):
        print("Entering into renew propert.html")
        """Render the renewal form for a specific property."""
        property_obj = get_object_or_404(RentalProperties, pk=pk)
        form = PropertyForm(instance=property_obj)
        agents = Users.objects.filter(is_active=True)
        receipt_nos = ManagementReceipts.objects.all()
        print("---- Rendering renew_property_page for Property ID:", pk)
        print("---- Cleaned Agent Names ----")
        for agent in agents:
            print(agent.name.strip() if agent.name else "No name")
        print("-----------------------------")
        print("----- Valid Receipt Numbers -----")
        # for rcpt in receipt_nos:
        #     print("Receipt Number",rcpt)
        print("----------------------------------")
        return render(request, 'home/renew.html', {
            'form': form,
            'property': property_obj,
            'agents': agents,
            'receipt_nos': receipt_nos
        })

    #Writing function for renew


    @action(detail=True, methods=['put'], url_path='renew')
    def renew(self, request, *args, **kwargs):
        print("Entered into renew.")
        property_obj = self.get_object()
        mutable_data = {
            key: request.data.getlist(key) if len(request.data.getlist(key)) > 1 else request.data.get(key)
            for key in request.data
        }
        mutable_data.update(request.FILES)

        # Remove file keys from mutable_data to avoid serializer conflict
        for key in request.FILES.keys():
            if key in mutable_data:
                del mutable_data[key]

        updated_files = {}
        is_renewal = mutable_data.get('is_renewal', 'false').lower() == 'true'
        reference_number = mutable_data.get('reference_number') or property_obj.reference_number
        path = f"rental/referencenumber_CP/{reference_number}"

        print(f"🔍 STARTING {'RENEW' if is_renewal else 'UPDATE'} for Property ID: {kwargs.get('pk')}")
        print(f"📁 Reference Path: {path}")
        print(f"📥 FILE KEYS: {list(request.FILES.keys())}")
        print(f"📝 FORM DATA: {dict(request.data)}")

        file_fields = [
            'pms_contract', 'owner_passport_copy', 'pms_cheque_copy',
            'title_deed', 'kyc_form', 'screening', 'owner_eid_copy',
            'poa_pp', 'poa_copy', 'key_hand_over_form'
        ]
        required_file_fields = [
            'pms_contract', 'owner_passport_copy', 'pms_cheque_copy',
            'title_deed', 'kyc_form'
        ]

        # Process file uploads (append only)
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
                    updated_files.setdefault(base_field_name, []).append(filepath)
                    print(f"✅ Uploaded: {filename}")
                else:
                    print(f"❌ Upload failed: {filename}")
                    return Response(
                        {"error": f"Failed to upload file: {filename}"},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )

        # Combine uploaded files + existing files - removed ones (if explicitly given)
        for field in file_fields:
            # Get existing files from DB or hidden input
            db_value = getattr(property_obj, field, "") or ""
            existing_values = mutable_data.get(f"{field}_existing_values", db_value)
            existing_files = [f.strip() for f in existing_values.split(",") if f.strip()]

            # Only remove files explicitly listed in <field>_removed
            removed_files = mutable_data.get(f"{field}_removed", "")
            removed_list = [f.strip() for f in removed_files.split(",") if f.strip()]
            existing_files = [f for f in existing_files if f not in removed_list]

            # Combine
            new_files = updated_files.get(field, [])
            final_files = existing_files + new_files
            mutable_data[field] = ",".join(final_files)
            print(f"🔄 Final {field}: {mutable_data[field]}")

            # Check required files
            if field in required_file_fields and not final_files:
                print(f"❌ Validation failed: {field} is required")
                return Response(
                    {"error": f"{field} is required."},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Handle cheque dates
        cheque_dates = []
        for key in mutable_data:
            if key.startswith("cheque_date["):
                date = mutable_data[key]
                if date:
                    cheque_dates.append(date)
        mutable_data["cheque_date"] = " ".join(cheque_dates) if cheque_dates else ""
        print(f"📅 Cheque Dates: {mutable_data['cheque_date']}")

        # Update receipt number if present
        if "receipt_no" in mutable_data and mutable_data["receipt_no"]:
            try:
                ManagementReceipts.objects.filter(id=mutable_data["receipt_no"]).update(
                    deal_refer_no=mutable_data["reference_number"]
                )
                ManagementReceipts.objects.filter(id=mutable_data["receipt_no"]).update(
                    status= "Used"
                )
                
                print(f"✅ Linked receipt_no to reference_number")
            except Exception as e:
                print(f"❌ Error updating receipt_no: {str(e)}")

        # Renewal-specific flags
        if is_renewal:
            mutable_data["submitted_by_user_id"] = str(request.user.id)
            mutable_data["submitted_date"] = datetime.date.today().isoformat()
            mutable_data["form_status"] = "Complete"
            mutable_data["is_approved_rejected"] = "P"
            mutable_data["is_entered_in_finance_system"] = "0"
            mutable_data["is_deleted"] = "N"
            print(f"📌 Renewal flags applied.")

        # Save with serializer
        serializer = self.get_serializer(property_obj, data=mutable_data, partial=True)
        if serializer.is_valid():
            serializer.save()
            print(f"✅ {'Renewed' if is_renewal else 'Updated'} successfully.")
            return Response(
                {"success": True, "data": serializer.data},
                status=status.HTTP_200_OK
            )
        else:
            print(f"❌ Serializer Error: {serializer.errors}")
            return Response(
                {"success": False, "message": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

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
   



    @action(detail=False, methods=['post'], url_path='filter')
    def datatable_filter(self, request):

        print(request.user , "request_user_fron hte data ")
        user =request.user
        print(request.user.account_id , "request_user_fron hte data ")
        account_id = request.user.account_id
    
        role = request.user.groups.all()  # This gives you Group model instances
        print("👥 Group count:", role)
        # print("gg",user_groups)
        print("✅ Groups user belongs to:", [group.name for group in role])
        roleofuser =""
        # Iterate over each group and print all model field names and their values
        for group in role:
            print(f"🔍 Meta fields for group: {group.name}")
            for field in group._meta.fields:
                field_name = field.name
               
                field_value = getattr(group, field_name)
                roleofuser = getattr(group, field_name)
                print(f"    {field_name}: {field_value}")
        

        data = filterSerializer(data=request.data)
        data.is_valid(raise_exception=True)
        data = data.validated_data

        
        print(account_id)
        is_manager = roleofuser == f'{account_id}-Manager'
        is_admin = roleofuser == f'{account_id}-Admin'
        is_finance = roleofuser == f'{account_id}-Finance'
        is_agent = roleofuser == f'{account_id}-Agent'
        
        print(is_manager)

        
        
        queryset = RentalProperties.objects.filter(is_deleted='N',account_id= account_id)
        

        # Global search
        search_term = data.get("search", {}).get("value") or ''
        if search_term:
            queryset = queryset.filter(
                Q(reference_number__icontains=search_term) |
                Q(building_name__icontains=search_term) |
                Q(project_name__icontains=search_term)
            )
            print("After global search:", queryset)

        

        filter_fields = {
            "reference_no": "reference_number",
            "building_name": "building_name",
            "unit_details": "unit_details",  # or "unit_details" depending on model field
            "project_name": "project_name",
            "property_id": "property_id",
            "approval_status": "approval_status",
            # add more mappings if needed
        }

        for key, model_field in filter_fields.items():
            value = data.get(key)
            if value:
                if key.endswith('_from'):
                    actual_field = model_field[:-5]
                    queryset = queryset.filter(**{f"{actual_field}__gte": value})
                elif key.endswith('_to'):
                    actual_field = model_field[:-3]
                    queryset = queryset.filter(**{f"{actual_field}__lte": value})
                else:
                    queryset = queryset.filter(**{f"{model_field}__icontains": value})

       
        #Now handle unit_details separately
        print("Validated data dictionary:", data)
        print("Initial queryset count:", queryset.count())
        print("Initial queryset query:", str(queryset.query))

        reference_no_val = data.get("reference_number")
        print("Reference number value from data:", reference_no_val)
        print("Queryset count before filtering reference_number:", queryset.count())

        if reference_no_val:
            print("Filtering queryset by reference_number:", reference_no_val)
            queryset = queryset.filter(reference_number__icontains=reference_no_val)
            print("Queryset count after filtering:", queryset.count())
        else:
            print("reference_number not found or empty in validated data.")

        unit_details_val = data.get("unit_details")  # or 'unit_no' if your frontend sends it, but model field is unit_details
        if unit_details_val:
            queryset = queryset.filter(unit_details__icontains=unit_details_val)
        else:
            print("Unit Number not found.")

        id_val = data.get("id")
        if id_val:
            queryset = queryset.filter(id=id_val)
        else:
            print("Property id is not found.")

        status_val = data.get("status")
        if status_val:
            queryset = queryset.filter(status__iexact=status_val)
        else:
            print("Status not found.")


        tenancy_start_date_val = data.get("tenancy_start_date")
        print(f"Raw tenancy_start_date value: {tenancy_start_date_val} (type: {type(tenancy_start_date_val)})")

        if tenancy_start_date_val:
            # If it's a date object, convert to string in dd-mm-yyyy format
            if isinstance(tenancy_start_date_val, date):
                date_str = tenancy_start_date_val.strftime("%d-%m-%Y")
                print(f"Converted tenancy_start_date to string (dd-mm-yyyy): {date_str}")
            else:
                # If it's already string, just use it directly (you can add validation here)
                date_str = tenancy_start_date_val
                print(f"Using tenancy_start_date string as is: {date_str}")

            queryset = queryset.filter(tenancy_start_date=date_str)
            print(f"Filtering queryset where tenancy_start_date = '{date_str}'")
        else:
            print("No tenancy_start_date provided, skipping filter.")

        tenancy_end_date_val = data.get("tenancy_end_date")
        print(f"Raw tenancy_end_date value: {tenancy_end_date_val} (type: {type(tenancy_end_date_val)})")

        if tenancy_end_date_val:
            if isinstance(tenancy_end_date_val, date):
                date_str = tenancy_end_date_val.strftime("%d-%m-%Y")
                print(f"Converted tenancy_end_date to string (dd-mm-yyyy): {date_str}")
            else:
                date_str = tenancy_end_date_val
                print(f"Using tenancy_end_date string as is: {date_str}")

            queryset = queryset.filter(tenancy_end_date=date_str)
            print(f"Filtering queryset where tenancy_end_date = '{date_str}'")
        else:
            print("No tenancy_end_date provided, skipping filter.")

        # pm_start_date
        pm_start_date_val = data.get("pm_start_date")
        print(f"Raw pm_start_date value: {pm_start_date_val} (type: {type(pm_start_date_val)})")
        if pm_start_date_val:
            if isinstance(pm_start_date_val, date):
                date_str = pm_start_date_val.strftime("%d-%m-%Y")
                print(f"Converted pm_start_date to string (dd-mm-yyyy): {date_str}")
            else:
                date_str = pm_start_date_val
                print(f"Using pm_start_date string as is: {date_str}")
            queryset = queryset.filter(pm_start_date=date_str)
            print(f"Filtering queryset where pm_start_date = '{date_str}'")
        else:
            print("No pm_start_date provided, skipping filter.")

        # pm_end_date
        pm_end_date_val = data.get("pm_end_date")
        print(f"Raw pm_end_date value: {pm_end_date_val} (type: {type(pm_end_date_val)})")
        if pm_end_date_val:
            if isinstance(pm_end_date_val, date):
                date_str = pm_end_date_val.strftime("%d-%m-%Y")
                print(f"Converted pm_end_date to string (dd-mm-yyyy): {date_str}")
            else:
                date_str = pm_end_date_val
                print(f"Using pm_end_date string as is: {date_str}")
            queryset = queryset.filter(pm_end_date=date_str)
            print(f"Filtering queryset where pm_end_date = '{date_str}'")
        else:
            print("No pm_end_date provided, skipping filter.")

        deal_date_val = data.get("deal_date")
        print(f"Raw deal_date value: {deal_date_val} (type: {type(deal_date_val)})")

        if deal_date_val:
            # If it's a date object, convert to string in dd-mm-yyyy format
            if isinstance(deal_date_val, date):
                date_str = deal_date_val.strftime("%d-%m-%Y")
                print(f"Converted deal_date to string (dd-mm-yyyy): {date_str}")
            else:
                # If it's already a string, just use it directly (you can add validation here)
                date_str = deal_date_val
                print(f"Using deal_date string as is: {date_str}")

            queryset = queryset.filter(deal_date=date_str)
            print(f"Filtering queryset where deal_date = '{date_str}'")
        else:
            print("No deal_date provided, skipping filter.")

       
        submitted_date_val = data.get("submitted_date")
        print(f"Parsed submitted_date: {submitted_date_val} (type: {type(submitted_date_val)})")

        if submitted_date_val:
            if isinstance(submitted_date_val, date):
                queryset = queryset.filter(submitted_date=submitted_date_val)
            else:
                # if somehow a string slipped through, try parsing
                try:
                    parsed_date = datetime.strptime(submitted_date_val, "%d-%m-%Y").date()
                except ValueError:
                    parsed_date = datetime.strptime(submitted_date_val, "%Y-%m-%d").date()
                queryset = queryset.filter(submitted_date=parsed_date)

        # Filteration on types keyword
        deal_type = data.get("type")
        print("Deal type:", deal_type)
        
        if deal_type:
            if deal_type == 'pending':
                if account_id:
                    if  is_manager or is_agent or user.is_superuser:
                        print('entered the  manage pending')
                        queryset = queryset.filter(manager_approved_rejected='P', form_status='Complete')
                    else:
                        print("entered the  finace pending")
                        queryset = queryset.filter(is_approved_rejected='P', manager_approved_rejected='A', form_status='Complete')
 
            elif deal_type == 'approved':
                #if role in [f'{account_id}-Manager', f'{account_id}-Agent',] or user.is_superuser:

                if is_manager or is_agent or user.is_superuser:
                    queryset = queryset.filter(manager_approved_rejected='A', form_status='Complete')
                else:
                    queryset = queryset.filter(is_approved_rejected='A' , form_status='Complete')
 
            elif deal_type == 'rejected':

                #if role in [f'{account_id}-Manager', f'{account_id}-Agent',] or user.is_superuser:
                if is_manager or is_agent or user.is_superuser:
                    queryset = queryset.filter( manager_approved_rejected='R', form_status='Complete')
                else:
                     queryset = queryset.filter(is_approved_rejected='R' , form_status='Complete')
               
 
            #Here waitint is related to Waiting for Waiting Finance
            elif deal_type == "waiting" :
                queryset = queryset.filter(is_approved_rejected='F')
 
            elif deal_type == 'entered-finance':
                queryset = queryset.filter(is_entered_in_finance_system='1',form_status= "Complete")
            
            #Here waiting-finance is related to pending finance
            elif deal_type == "waiting-finance" :
                queryset = queryset.filter(is_entered_in_finance_system='0' ,form_status = "Complete")
 
            elif deal_type == 'draft':
                queryset = queryset.filter(form_status='Incomplete',submitted_by_user_id=user.id)
       
            elif deal_type == "All" :
                queryset = queryset.filter(form_status = "Complete")  
 
            if is_admin and deal_type == 'draft':
                queryset = queryset.filter(created_by=user.email)

            if is_agent :
                queryset = queryset.filter(submitted_by_user_id=user.id)
            elif is_admin and deal_type == "draft":
                queryset = queryset.filter(created_by=user.email)
            else:
                role = "superadmin"
 
 
        else:
            print("Invalid deal type received")
            return Response({"error": "Invalid deal type"}, status=400)
        #print("After deal type filter:", queryset)

        # Date range filter
        if data.get("from"):
            queryset = queryset.filter(date__gte=data.get("from"))
            print("After from date filter:", queryset)
        if data.get("to"):
            queryset = queryset.filter(date__lte=data.get("to"))
            print("After to date filter:", queryset)

        # ✅ Ordering Logic
        order = request.data.get("order", [{}])[0]  # ⬅️ Use raw request.data
        #print("Order parameter:", order)

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
                    #print("✅ Ordering applied. SQL:", str(queryset.query))

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
        #print("Paginated queryset:", paginated)

        # Prepare final response
        response_data = {
            "draw": int(data.get("draw", 0)),
            "recordsTotal": queryset.count(),
            "recordsFiltered": queryset.count(),
            "data": DealSerializer(paginated, many=True, context={"request": request}).data,
            "input": request.data.copy()
        }

        #print("📦 Final response data preview:", response_data)
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



@login_required(login_url="/login/")
def all_rental_properties(request):
    print("User authenticated:", request.user.is_authenticated)
    print("User:", request.user)
    print("Is anonymous:", request.user.is_anonymous)
    """
    View to list all rental deals.
    """
    path = request.path
    if path == '/rental-properties/draft/':
        properties = RentalProperties.objects.filter(form_status='Incomplete')
    else:
        properties = RentalProperties.objects.all()

    #logger.debug(f"Queryset count: {properties.count()}")
    if properties.count() == 0:
        logger.warning("⚠️ No properties found in queryset")
    else:
        for property_obj in properties:
            property_obj.update_status_if_needed()
    
    return render(request, 'home/propertyall.html', {'properties': properties})

def draft_property_list(request):
    drafts = RentalProperties.objects.filter(form_status='Incomplete', is_deleted='N')
    return render(request, 'home/draft_property_list.html', {'drafts': drafts})


#Manager recipts code
    

@login_required
def management_receipts_manager(request):
    return render(request, 'home/Manager.html')

def edit_management_receipt(request, pk):
    receipt = get_object_or_404(ManagementReceipts, pk=pk)
    return render(request, 'home/Manager_Edit.html', {'receipt': receipt})

class ManagementReceiptsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ManagementReceiptsFilterSerializer
    queryset = ManagementReceipts.objects.all()

    
    @action(detail=False, methods=['post'], url_path='managerdatatablefilter')
    def managerdatatablefilter(self, request):
        print("📥 Raw Request Data:", request.data)

        serializer = ManagementReceiptsFilterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        print("✅ Validated Filter Data:", data)

        queryset = ManagementReceipts.objects.filter(account_id = request.user.account_id)
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
            "agent_name", "unit_number", "building_name","date","sec_date"
        ]
        
        def parse_date_field(value):
            print(f"🔍 Received value: {value} (type: {type(value)})")

            if isinstance(value, date):
                print(f"✅ Value is already a date object, returning as-is: {value}")
                return value

            try:
                print("📅 Attempting to parse value as YYYY-MM-DD string...")
                parsed_date = datetime.strptime(value, "%Y-%m-%d").date()
                print(f"✅ Successfully parsed date: {parsed_date}")
                return parsed_date
            except Exception as e:
                print(f"❌ Failed to parse date. Error: {e}")
                return None
        for field in filter_fields:
            value = data.get(field)
            if value:
                print(f"🔧 Applying filter -> {field}: {value}")
                filter_kwargs = {f"{field}__icontains": value}
                queryset = queryset.filter(**filter_kwargs)
                print(f"   🔢 Count after {field} filter: {queryset.count()}")

            else:
                print("Value not found:",value)
        print("Full incoming data:", data)

        from_date_str = data.get('from')
        to_date_str = data.get('to')

        def parse_date_field(value):
            if not value:
                return None
            try:
                # Frontend should send date in 'YYYY-MM-DD' format
                return datetime.strptime(value, "%Y-%m-%d").date()
            except Exception:
                print(f"Failed to parse date: {value}")
                return None

        
        from_date = data.get('date')
        to_date = data.get('sec_date')

        print(f"📅 From date (validated): {from_date}")
        print(f"📅 To date (validated): {to_date}")


        print("From date:",from_date)
        print("To date:",to_date)

        if from_date and to_date:
            if from_date > to_date:
                return Response({"error": "'from' date cannot be after 'to' date"}, status=400)
                
                
        if from_date:
            queryset = queryset.filter(date__gte=from_date)
        else:
            print("No from date found")
        
        if to_date:
            queryset = queryset.filter(date__lte=to_date)


        
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
        return render(request, 'home/Manager_View.html', {'receipt': receipt})
    
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
    
    # @action(detail=False, methods=['get'], url_path='create-form')
    # def create_form(self, request):
    #     # Generate the next receipt number
    #     last_receipt = ManagementReceipts.objects.order_by('-receipt_number').first()
    #     next_receipt_number = int(last_receipt.receipt_number) + 1 if last_receipt else 1000
    #     return render(request, 'home/Manager_Create.html', {'next_receipt_number': next_receipt_number})

    @action(detail=False, methods=['get'], url_path='create-form')
    def create_form(self, request):
        # Order numerically, not lexicographically
        last_receipt = (
            ManagementReceipts.objects
            .annotate(receipt_num_int=Cast('receipt_number', IntegerField()))
            .order_by('-receipt_num_int')
            .first()
        )
 
        if last_receipt and last_receipt.receipt_number and last_receipt.receipt_number:
            next_receipt_number = str(int(last_receipt.receipt_number) + 1)  # 👈 keep as string
        else:
            next_receipt_number = "1000"  # 👈 starting baseline, still string
 
        return render(request, 'home/Manager_Create.html', {
            'next_receipt_number': next_receipt_number
        })

    @action(detail=False, methods=['post'], url_path='create')
    def create_receipt(self, request):
        print("DEBUG: create_receipt hit", request.data)
        mutable_data = request.data.copy()
        if request.user.account_id:
            print("DEBUG: Account ID", request.user.account_id)
            mutable_data["account_id"] = request.user.account_id
        else:
            return Response({
                'success': False,
                'message': 'User has no linked account.',
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer = ManagementReceiptsSerializer(data=mutable_data)
        if serializer.is_valid():
            try:
                serializer.save()
                print("DEBUG: Data saved successfully", serializer.data)
                return Response({
                    'success': True,
                    'message': 'Receipt created successfully.'
                }, status=status.HTTP_201_CREATED)
            except Exception as e:
                print("DEBUG: Error during save", str(e))
                return Response({
                    'success': False,
                    'message': f'Failed to save receipt: {str(e)}',
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
        print("DEBUG: Serializer errors", serializer.errors)
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
        
 