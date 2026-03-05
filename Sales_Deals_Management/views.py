import datetime
from linecache import cache
import logging
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
from Rental_Deal.Utilities import upload_file_to_full_s3_url, delete_from_s3, s3_file_exists
import boto3
from django.db import transaction


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

logger = logging.getLogger('Sales_Deals_Management')


# ========== S3 Configuration & Utility Functions ==========
s3 = boto3.client(
    "s3",
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_S3_REGION_NAME
)

BUCKET_NAME = "deal-saas"


def copy_reference_folder(old_ref, new_ref):
    """
    Copy S3 folder from old reference to new reference.
    Supports CPS, CPM, CPMR, CP, CPR prefixes.
    """
    print(f"Starting S3 folder copy from {old_ref} to {new_ref}")
    try:
        # Extract prefix from old reference (before the dash)
         
        
        old_prefix = f"live/classic_properties/sale/referencenumber_CPS/{old_ref}/"
        new_prefix = f"live/classic_properties/sale/referencenumber_CPS/{new_ref}/"

        print(old_prefix)
        # Check if the new reference folder already exists in S3
        paginator_check = s3.get_paginator("list_objects_v2")
        new_folder_exists = False
        print(new_prefix)
        
        for page in paginator_check.paginate(Bucket=BUCKET_NAME, Prefix=new_prefix, MaxKeys=1):
            if "Contents" in page:
                new_folder_exists = True
                break
        
        if new_folder_exists:
            logger.info(f"Folder already exists for new reference: {new_ref}. Skipping file copy.")
            return True

        paginator = s3.get_paginator("list_objects_v2")

        print( "new_floder_exists", new_folder_exists)

        for page in paginator.paginate(Bucket=BUCKET_NAME, Prefix=old_prefix):
            if "Contents" not in page:
                logger.info(f"No files found in S3 for reference: {old_ref}")
                return

            for obj in page["Contents"]:
                old_key = obj["Key"]

                # Replace only the first occurrence
                new_key = old_key.replace(old_prefix, new_prefix, 1)

                s3.copy_object(
                    Bucket=BUCKET_NAME,
                    CopySource={"Bucket": BUCKET_NAME, "Key": old_key},
                    Key=new_key
                )

                logger.info(f"Copied: {old_key} → {new_key}")

        logger.info("S3 Folder copy completed successfully.")
        return True
    except Exception as e:
        logger.error(f"Error copying S3 folder: {str(e)}")
        print(f"Error copying S3 folder: {str(e)}")
        raise


@transaction.atomic
def clone_deal_with_new_reference(old_deal_id, new_reference):
    """
    Clone a deal with a new reference number.
    Steps:
    1. Soft delete the original deal first (to avoid conflicts)
    2. Check if new reference already exists
    3. Copy S3 files from old reference to new reference
    4. Create a new deal record with updated reference
    5. Update receipts with new deal reference
    """
    try:
        # 1️⃣ Get the old deal and store its original reference
        old_deal = SalesDeals.objects.get(id=old_deal_id)
        old_reference = old_deal.reference_number
        logger.info(f"Cloning deal {old_deal_id} with reference: {old_reference}")

        # Store receipt IDs before modifying the old deal
        receipt_ids = [old_deal.receipt_id, old_deal.receipt_id2, old_deal.receipt_id3]
        receipt_ids = [rid for rid in receipt_ids if str(rid).isdigit() and int(rid) > 0]

        # 2️⃣ Soft delete the old deal immediately (rename it to avoid conflicts)
        old_deal.is_deleted = "Y"
        old_deal.reference_number = old_reference + "D"
        old_deal.save()
        logger.info(f"Soft deleted old deal. Updated reference to: {old_deal.reference_number}")

        # 3️⃣ Check if new reference already exists (check both dash and slash variations)
        # For example, if new_reference is "CPS-204", also check for "CPS/204"
        new_reference_dash = new_reference.replace("/", "-")
        new_reference_slash = new_reference.replace("-", "/")
        
        if SalesDeals.objects.filter(
            Q(reference_number=new_reference) | 
            Q(reference_number=new_reference_dash) | 
            Q(reference_number=new_reference_slash)
        ).filter(is_deleted='N').exists():
            raise ValueError(f"Reference number {new_reference} already exists. Please choose a unique reference number.")

        # 4️⃣ Copy S3 files from old reference to new reference
        copy_reference_folder(old_reference, new_reference)

        # 5️⃣ Create new deal (clone from the original values)
        new_deal = SalesDeals.objects.get(id=old_deal_id)  # Get the original data again
        new_deal.pk = None  # This makes it a new record
        new_deal.reference_number = new_reference
        new_deal.is_deleted = "N"
        new_deal.save()
        
        logger.info(f"Created new deal with ID: {new_deal.id}, reference: {new_reference}")
        
        # 6️⃣ Update receipts with new deal reference
        if receipt_ids:
            Receipts.objects.filter(id__in=receipt_ids).update(
                deal_refer_no=new_reference,
                status='Used'
            )
            logger.info(f"Updated {len(receipt_ids)} receipts with new reference: {new_reference}")
        
        logger.info(f"Deal cloned successfully. New reference: {new_reference}, Deal ID: {new_deal.id}")
        return new_deal
    except Exception as e:
        logger.error(f"Error cloning deal: {str(e)}")
        raise



class SalesDealViewSet(viewsets.ModelViewSet):
    # queryset = SalesDeals.objects.all()
    serializer_class = SalesDealSerializer
    permission_classes = [IsAuthenticated]
    

    @action(detail=True, methods=['delete'], url_path='delete')
    def delete_sales(self, request, pk=None):
        sales = get_object_or_404(SalesDeals, pk=pk)

        receipt_ids = [sales.receipt_id, sales.receipt_id2, sales.receipt_id3]
        receipt_ids = [rid for rid in receipt_ids if str(rid).isdigit() and int(rid) > 0]  # Filter out null/zero values
        
        if receipt_ids:
            Receipts.objects.filter(id__in=receipt_ids).update(status='Unused', deal_refer_no='')

        SalesDeals.objects.filter(pk=pk).update(is_deleted='Y')
        SalesDeals.objects.filter(pk=pk).update(reference_number= sales.reference_number+"D")
        return Response(status=status.HTTP_204_NO_CONTENT)


    @action(detail=True, methods=['post'], url_path='clone-with-reference')
    def clone_deal_with_new_ref(self, request, pk=None):
        """
        API endpoint to clone a deal with a new reference number.
        
        POST /api/sales-deals/{id}/clone-with-reference/
        
        Request body:
        {
            "new_reference": "CPS-123456"
        }
        
        Returns:
        {
            "status": "success",
            "message": "Deal cloned successfully",
            "new_deal_id": 123,
            "new_reference": "CPS-123456"
        }
        """
        try:
            # Get new reference from request body
            new_reference = request.data.get('new_reference')
            
            if not new_reference:
                return Response(
                    {
                        "status": "error",
                        "message": "new_reference is required in request body"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Validate reference format (should contain dash)
            if '-' not in new_reference:
                return Response(
                    {
                        "status": "error",
                        "message": "Invalid reference format. Please use format like 'CPM-12345'"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Clone the deal
            new_deal = clone_deal_with_new_reference(pk, new_reference)
            
            # Get receipt count for the new deal
            receipt_count = 0
            receipt_ids = [new_deal.receipt_id, new_deal.receipt_id2, new_deal.receipt_id3]
            receipt_count = len([rid for rid in receipt_ids if str(rid).isdigit() and int(rid) > 0])
            
            return Response(
                {
                    "status": "success",
                    "message": "Deal cloned successfully",
                    "new_deal_id": new_deal.id,
                    "new_reference": new_deal.reference_number,
                    "receipts_updated": receipt_count
                },
                status=status.HTTP_201_CREATED
            )
            
        except ValueError as e:
            logger.warning(f"Validation error when cloning deal {pk}: {str(e)}")
            return Response(
                {
                    "status": "error",
                    "message": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        except SalesDeals.DoesNotExist:
            logger.error(f"Deal not found with id: {pk}")
            return Response(
                {
                    "status": "error",
                    "message": f"Deal with ID {pk} not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error cloning deal {pk}: {str(e)}")
            return Response(
                {
                    "status": "error",
                    "message": f"An error occurred while cloning the deal: {str(e)}"
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['get'], url_path='view')
    def view_sales_deal(self, request, pk=None):


        def get_receipt_info(receipt_no):
            """
            Returns (receipt_no_output, receipt_id)
            based on your business logic.
            """
            if receipt_no in ["Null", ""," ", None]:
                return "Null", ""

            if receipt_no == "No Commission":
                return "No Commission", ""

            # Find receipt
            rec = Receipts.objects.filter(receipt_number=receipt_no).first()
            if rec:
                return rec.receipt_number, rec.id

            return "", ""






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
            
         

        elif sales_deal.receipt_no == "No Commission" or sales_deal.receipt_no == "No Commision":
            # Case 2: No Commission special case
            recipt_no = "No Comission"
            recipt_id = ""
            

        

        else:
            print("entered else case ")
            # Case 3: Receipt ID
            recipt = Receipts.objects.filter(receipt_number=sales_deal.receipt_no).first()
            if recipt:
                print("entered if case ")
                recipt_no = recipt.receipt_number
                recipt_id = recipt.id
                print(recipt_no , "this is recipt number ")
                print(recipt_id , "this is recipt id ")
            else:
                recipt_no = ""
                recipt_id = ""


        recipt_no_1, recipt_id_1 = get_receipt_info(sales_deal.receipt_no)
        # Receipt No 2
        recipt_no_2, recipt_id_2 = get_receipt_info(sales_deal.receipt_no2)

        # Receipt No 3
        recipt_no_3, recipt_id_3 = get_receipt_info(sales_deal.receipt_no3)

        recipt_no_4, recipt_id_4 = get_receipt_info(sales_deal.receipt_no4)

        recipt_no_5, recipt_id_5 = get_receipt_info(sales_deal.receipt_no5) 
        
        return render(request, 'home/viewsalesdeal.html', {'salesdeal': serializer.data, 'aws_base_url': aws_url, "receipt_no": recipt_no, "receipt_id": recipt_id,  
                                                           "receipt_no_2":recipt_no_2 , "receipt_id_2":recipt_id_2 ,
        "receipt_no_3":recipt_no_3 , "receipt_id_3":recipt_id_3,
        "receipt_no_4":recipt_no_4 , "receipt_id_4":recipt_id_4,
        "receipt_no_5":recipt_no_5 , "receipt_id_5":recipt_id_5})

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
                reccicpt = Receipts.objects.filter(id=receipt_id)

                Receipts.objects.filter(id=mutable_data['receipt_no']).update(status="Used")
                print(f"Updated receipt_no {receipt_id} with reference_number {mutable_data['reference_number']}")

                mutable_data['receipt_id'] = receipt_id
                mutable_data['receipt_no'] = reccicpt[0].receipt_number


            else:
                pass
        except (ValueError, TypeError):
            print("Invalid receipt_no or not provided, skipping update.")

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
        
        if mutable_data.get('receipt_no4'):
                if mutable_data['receipt_no4'].isdigit():
                    print("this is the receipt no4", mutable_data['receipt_no4'])
                    Receipts.objects.filter(id=mutable_data['receipt_no4']).update(deal_refer_no=mutable_data['reference_number'])
                    Receipts.objects.filter(id=mutable_data['receipt_no4']).update(status="Used")

                    reccicpt4 = Receipts.objects.filter(id=mutable_data['receipt_no4']).first()
                    mutable_data['receipt_id4'] = reccicpt4.id
                    mutable_data['receipt_no4'] = reccicpt4.receipt_number
                    print("this is the receipt id4", mutable_data['receipt_id4'])
                    print("this is the receipt no4", mutable_data['receipt_no4'])
                else:
                    pass
        
        if mutable_data.get('receipt_no5'):
                if mutable_data['receipt_no5'].isdigit():
                    print("this is the receipt no5", mutable_data['receipt_no5'])
                    Receipts.objects.filter(id=mutable_data['receipt_no5']).update(deal_refer_no=mutable_data['reference_number'])
                    Receipts.objects.filter(id=mutable_data['receipt_no5']).update(status="Used")

                    reccicpt5 = Receipts.objects.filter(id=mutable_data['receipt_no5']).first()
                    mutable_data['receipt_id5'] = reccicpt5.id
                    mutable_data['receipt_no5'] = reccicpt5.receipt_number
                    print("this is the receipt id5", mutable_data['receipt_id5'])
                    print("this is the receipt no5", mutable_data['receipt_no5'])
                else:
                    pass


        print(mutable_data)

        # mutable_data['submitted_by_user'] = request.user.id
        mutable_data['account'] = request.user.account_id
        mutable_data['created_by'] = request.user.id
        # mutable_data['submitted_by_agent'] = request.user.id

        if not mutable_data.get('submitted_by_agent'):
            mutable_data['submitted_by_user'] = request.user.id
            mutable_data['submitted_by_agent'] = request.user.id

        else :
            mutable_data['submitted_by_user'] = mutable_data.get('submitted_by_agent')
           
       
           


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
            reference_number = mutable_data.get("reference_number").strip()
            path_folder = f"sale/referencenumber_CPS/{reference_number}"

       

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
                    return Response({"detail": f"Failed to upload file {filename}. Please try again.uploading"} , status=status.HTTP_400_BAD_REQUEST)

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

        # thsis is to check if the fiel are present in the s3 bucket or not
        for key, value in final_updated_values.items():
            print(f"Final updated value - {key}: {value}")

       
       
        missing_files = []
        for base_field_name, files_str in final_updated_values.items():
            for fname in files_str.split(","):
                relative_path = f"sale/referencenumber_CPS/{mutable_data['reference_number'].strip()}/{fname}"
                if not s3_file_exists(relative_path):
                    missing_files.append(fname)

         
        
        if missing_files:
            logger.error("Missing files before update for rental id=%s missing=%s", SalesDeals.pk, missing_files)
            return Response(
                {"detail": f"The following files are missing in S3: {', '.join(missing_files)} upload again"},
                status=status.HTTP_400_BAD_REQUEST
            )



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
                reference_number = mutable_data.get("reference_number").strip()
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
                        # is_deleted = delete_from_s3(relative_path)
                        # if not is_deleted:
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
                    else : 
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
                is_submitted_date = getattr(sales_deal, 'submitted_date' , "")
                form_status = getattr(sales_deal, 'form_status', "")
                print("is_submitted_date", is_submitted_date)
                if  (not is_submitted_date and role in ["Agent"]):
                    print("submitted date already set so not updating", is_submitted_date)
                    mutable_data['submitted_date']= datetime.date.today()
                elif (form_status == "Incomplete" and role in ["Agent"] and is_submitted_date) :
                     mutable_data['submitted_date']= datetime.date.today()
                    # handle resubmited date block
                elif is_submitted_date and role in ["Agent"]:
                    mutable_data['re_submitted_date']= datetime.date.today()
                    print("this is resubmitted date block", mutable_data['re_submitted_date'])
                    mutable_data['is_approved_rejected'] = "P"  # set to pending on resubmission
                    mutable_data['manager_approved_rejected'] = "P"  # set to pending on resubmission
                
            else:
                mutable_data['form_status'] = "Incomplete"
            print(f"DEBUG: form_status set to: {mutable_data['form_status']}")


            if mutable_data.get("is_approved_rejected") and mutable_data.get("is_approved_rejected") in ["A", "R", "F"]:
                mutable_data['approved_rejected_by'] = request.user.email
            
            if mutable_data.get('receipt_no') is not None:
                get_receipt_no_db = getattr(sales_deal, 'receipt_no', "")
                get_receipt_id_db = getattr(sales_deal, 'receipt_id', "")
                print("get_receipt_no_db", get_receipt_no_db)
                print("get_receipt_id_db", get_receipt_id_db)

                receipt_value = str(mutable_data.get('receipt_no')).strip()

                if receipt_value.isdigit():
                    if str(get_receipt_id_db) != receipt_value:
                        if str(get_receipt_id_db).isdigit():
                            # Here we dont need to check the NOne case because it is having 0
                            Receipts.objects.filter(id=get_receipt_id_db).update(status="Unused", deal_refer_no="")

                        print("this is the receipt no", receipt_value)
                        Receipts.objects.filter(id=receipt_value).update(deal_refer_no=mutable_data['reference_number'])
                        Receipts.objects.filter(id=receipt_value).update(status="Used")

                        reccicpt = Receipts.objects.filter(id=receipt_value).first()
                        if reccicpt:
                            mutable_data['receipt_id'] = reccicpt.id
                            mutable_data['receipt_no'] = reccicpt.receipt_number
                    if str(get_receipt_id_db) == receipt_value:
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
                get_receipt_no2_db = getattr(sales_deal, 'receipt_no2', "")
                get_receipt_id2_db = getattr(sales_deal, 'receipt_id2', "")
                print("get_receipt_no2_db", get_receipt_no2_db)
                print("get_receipt_id2_db", get_receipt_id2_db)

                receipt_value2 = str(mutable_data.get('receipt_no2')).strip()

                if receipt_value2.isdigit():
                    if str(get_receipt_id2_db) != receipt_value2:
                        if str(get_receipt_id2_db).isdigit() or str(get_receipt_id2_db) == "None":
                            # here we need to check the None case because we are having Null in DB 
                            if str(get_receipt_id2_db).isdigit():
                                Receipts.objects.filter(id=get_receipt_id2_db).update(status="Unused", deal_refer_no="")

                        print("this is the receipt no2", receipt_value2)
                        Receipts.objects.filter(id=receipt_value2).update(deal_refer_no=mutable_data['reference_number'])
                        Receipts.objects.filter(id=receipt_value2).update(status="Used")

                        reccicpt2 = Receipts.objects.filter(id=receipt_value2).first()
                        if reccicpt2:
                            mutable_data['receipt_id2'] = reccicpt2.id
                            mutable_data['receipt_no2'] = reccicpt2.receipt_number
                    if str(get_receipt_id2_db) == receipt_value2:
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
                get_receipt_no3_db = getattr(sales_deal, 'receipt_no3', "")
                get_receipt_id3_db = getattr(sales_deal, 'receipt_id3', "")
                print("get_receipt_no3_db", get_receipt_no3_db)
                print("get_receipt_id3_db", get_receipt_id3_db)

                receipt_value3 = str(mutable_data.get('receipt_no3')).strip()

                if receipt_value3.isdigit():
                    if str(get_receipt_id3_db) != receipt_value3:
                        if str(get_receipt_id3_db).isdigit() or str(get_receipt_id3_db) == "None":
                            # here we need to check the None case because we are having Null in DB 
                            if str(get_receipt_id3_db).isdigit():
                                Receipts.objects.filter(id=get_receipt_id3_db).update(status="Unused", deal_refer_no="")

                        print("this is the receipt no3", receipt_value3)
                        Receipts.objects.filter(id=receipt_value3).update(deal_refer_no=mutable_data['reference_number'])
                        Receipts.objects.filter(id=receipt_value3).update(status="Used")

                        reccicpt3 = Receipts.objects.filter(id=receipt_value3).first()
                        if reccicpt3:
                            mutable_data['receipt_id3'] = reccicpt3.id
                            mutable_data['receipt_no3'] = reccicpt3.receipt_number

                    if str(get_receipt_id3_db) == receipt_value3:
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
            

            if mutable_data.get('receipt_no4') is not None:
                get_receipt_no4_db = getattr(sales_deal, 'receipt_no4', "")
                get_receipt_id4_db = getattr(sales_deal, 'receipt_id4', "")
                print("get_receipt_no4_db", get_receipt_no4_db)
                print("get_receipt_id4_db", get_receipt_id4_db)

                receipt_value4 = str(mutable_data.get('receipt_no4')).strip()   
                if receipt_value4.isdigit():
                    if str(get_receipt_id4_db) != receipt_value4:
                        if str(get_receipt_id4_db).isdigit() or str(get_receipt_id4_db) == "None":
                            if str(get_receipt_id4_db).isdigit():
                                Receipts.objects.filter(id=get_receipt_id4_db).update(status="Unused", deal_refer_no="")

                        print("this is the receipt no4", receipt_value4)
                        Receipts.objects.filter(id=receipt_value4).update(deal_refer_no=mutable_data['reference_number'])
                        Receipts.objects.filter(id=receipt_value4).update(status="Used")

                        reccicpt4 = Receipts.objects.filter(id=receipt_value4).first()      
                        if reccicpt4:
                            mutable_data['receipt_id4'] = reccicpt4.id
                            mutable_data['receipt_no4'] = reccicpt4.receipt_number  
                    if str(get_receipt_id4_db) == receipt_value4:
                        reccicpt4 = Receipts.objects.filter(id=receipt_value4).first()      
                        if reccicpt4:
                            mutable_data['receipt_id4'] = reccicpt4.id
                            mutable_data['receipt_no4'] = reccicpt4.receipt_number
                else:
                    if receipt_value4 in ["Null", "No Commission", ""]:
                        if str(get_receipt_id4_db).isdigit():
                            Receipts.objects.filter(id=get_receipt_id4_db).update(status="Unused", deal_refer_no="")
                        mutable_data['receipt_id4'] = 0
                        mutable_data['receipt_no4'] = receipt_value4

            if mutable_data.get('receipt_no5') is not None:
                get_receipt_no5_db = getattr(sales_deal, 'receipt_no5', "")
                get_receipt_id5_db = getattr(sales_deal, 'receipt_id5', "")
                print("get_receipt_no5_db", get_receipt_no5_db)
                print("get_receipt_id5_db", get_receipt_id5_db)

                receipt_value5 = str(mutable_data.get('receipt_no5')).strip()   
                if receipt_value5.isdigit():
                    if str(get_receipt_id5_db) != receipt_value5:
                        if str(get_receipt_id5_db).isdigit() or str(get_receipt_id5_db) == "None":
                            if str(get_receipt_id5_db).isdigit():
                                Receipts.objects.filter(id=get_receipt_id5_db).update(status="Unused", deal_refer_no="")

                        print("this is the receipt no5", receipt_value5)
                        Receipts.objects.filter(id=receipt_value5).update(deal_refer_no=mutable_data['reference_number'])
                        Receipts.objects.filter(id=receipt_value5).update(status="Used")

                        reccicpt5 = Receipts.objects.filter(id=receipt_value5).first()      
                        if reccicpt5:
                            mutable_data['receipt_id5'] = reccicpt5.id
                            mutable_data['receipt_no5'] = reccicpt5.receipt_number  
                    if str(get_receipt_id5_db) == receipt_value5:
                        reccicpt5 = Receipts.objects.filter(id=receipt_value5).first()      
                        if reccicpt5:
                            mutable_data['receipt_id5'] = reccicpt5.id
                            mutable_data['receipt_no5'] = reccicpt5.receipt_number
                else:
                    if receipt_value5 in ["Null", "No Commission", ""]:
                        if str(get_receipt_id5_db).isdigit():
                            Receipts.objects.filter(id=get_receipt_id5_db).update(status="Unused", deal_refer_no="")
                        mutable_data['receipt_id5'] = 0
                        mutable_data['receipt_no5'] = receipt_value5
 
            mutable_data['updated_by'] = request.user.email
            mutable_data['updated_at'] = now()

            if not mutable_data.get('submitted_by_agent'):
                mutable_data['submitted_by_user'] = request.user.id

            else :
                mutable_data['submitted_by_user'] = mutable_data.get('submitted_by_agent')

            
            
                 
                       

            print("mutable_data", mutable_data)
            # Now pass this updated data to serializer

            for key, value in final_updated_values.items():
                print(f"Final updated value - {key}: {value}")

            
            missing_files = []
            for base_field_name, files_str in final_updated_values.items():
                for fname in files_str.split(","):
                    if fname.strip():
                        relative_path = f"sale/referencenumber_CPS/{mutable_data['reference_number'].strip()}/{fname}"
                        if not s3_file_exists(relative_path):
                            missing_files.append(fname)
            
            if missing_files:
                return Response(
                    {"detail": f"The following files are missing in S3: {', '.join(missing_files)} upload again"},
                    status=status.HTTP_400_BAD_REQUEST
                )



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
    .order_by("-id").only(    "id",
    "account_id",
    "reference_number",
      # if you have this field in your model

    # Deal info
    "date",                     # Deal Date
    "submitted_date",           # Submission / Start Date
    "deal_amount",              # Deal Amount / Rental Price
    "project_name",
    "builduing_name",
    "unit_details",

    # Approval / status info
    "form_status",
    "manager_approved_rejected",
    "is_approved_rejected", 
    "approved_rejected_by",
    "is_deleted",

    # Submitted by user (related table)
    "submitted_by_user",
    "submitted_by_user__email",
    "submitted_by_user__name",

    # Owner (Seller) info
    "seller_name",
    "seller_source",
    "selller_mobile",
    "seller_email",
    "seller_nationality",
    "seller_agency",
    "seller_agent_name",
    "seller_agent_phone",
    "seller_agent_email",
    "seller_agency_brn",

    # Tenant (Buyer) info
    "buyer_name",
    "buyer_source",
    "buyer_mobile",
    "buyer_email",
    "buyer_nationality",
    "buyer_agency",
    "buyer_agent_name",
    "buyer_agent_phone",
    "buyer_agent_email",
    "buyer_agency_brn",

    # Mediating agency info
    "mediating_agency",
    "mediating_agent_name",
    "mediating_agent_phone",
    "mediating_agent_email",
    "mediating_agency_brn",

    # Commission info
    "total_commission",
    "less_outsude_commission",
    "net_commission",
    "classic",
    "agent1",
    "agent2",
    "agent3",
    "agent_name1",
    "agent_name2",
    "agent_name3",

    # Finance info
    "receipt_no",
    "kyc_number",
    "is_sale_aml",
    "is_entered_in_finance_system",

    # Comments & metadata
    "comments",
    "agent_comment",
    "comments_finance",
    "created_at",
    "created_by",
    "updated_by",  
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
            normalized_search_replace_slash = search_term.replace("/", "-")
            normalized_search_replace_minus = search_term.replace("-", "/")
            queryset = queryset.filter(
                Q(submitted_by_user__email__icontains=search_term) |
                Q(reference_number__icontains=search_term) |
                Q(reference_number__icontains=normalized_search_replace_slash) |
                Q(reference_number__icontains=normalized_search_replace_minus) |
                Q(date__icontains=search_term) |
                Q(unit_details__icontains=search_term) |
                Q(builduing_name__icontains=search_term) |
                Q(project_name__icontains=search_term) |
                Q(unit_details__icontains=search_term) |
                Q(seller_name__icontains=search_term) |

                Q(deal_amount__icontains=search_term) |
                Q(submitted_date__icontains=search_term)
            )
            print("Search Term:", search_term)  # Debugging line
        # Debugging line
        # Field-specific filters
        filter_fields = [
            "reference_number", "unit_details", "builduing_name","seller_source","selller_mobile"
            "is_approved_rejected", "project_name","seller_name","buyer_name","buyer_mobile","buyer_source",
           ]
        for field in filter_fields:
            value = validated.get(field)
            if value:
                print(f"Filtering {field} by {value}")  # Debugging line
                queryset = queryset.filter(**{f"{field}__icontains": value})

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
                    elif role not in ["Agent"]:
                        queryset = queryset.filter(is_approved_rejected="A", form_status="Complete")
                else:
                    return Response({"detail": "You do not have permission: view_approved_sales_deals"}, status=status.HTTP_403_FORBIDDEN)

            # ---------------- Rejected ----------------
            elif type_filter == "rejected":
                if user.has_perm("core.view_rejected_sales_deals"):
                    if account_id and (role in ["Manager"] or user.is_superuser):
                        queryset = queryset.filter(manager_approved_rejected="R", form_status="Complete")
                    elif role not in ["Agent"]:
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
                    queryset = queryset.filter(is_entered_in_finance_system="1", form_status="Complete",is_approved_rejected__in = ["A","F"])
                else:
                    return Response({"detail": "You do not have permission: enter_finance_sales_deal"}, status=status.HTTP_403_FORBIDDEN)

            # ---------------- Pending Finance ----------------
            elif type_filter == "pending-finance":
                if user.has_perm("core.view_pending_finance_sales_deal"):
                    queryset = queryset.filter(is_entered_in_finance_system="0", form_status="Complete",is_approved_rejected__in = ["A","F"])
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
                print("inside agent role filter")
                queryset = queryset.filter(submitted_by_user=user)

                if type_filter == "rejected":
                    print("inside rejected filter")
                    queryset = queryset.filter(Q(is_approved_rejected="R") | Q(manager_approved_rejected="R"), form_status="Complete")
                elif type_filter == "approved":
                    queryset = queryset.filter(is_approved_rejected="A", form_status="Complete")

            elif (role == "Admin" or user_role == "Admin") and type_filter == "draft":
                queryset = queryset.filter(created_by=user.email)
            else:
                role = "superadmin"

        # Date range filter

        if validated.get("from_date"):
            queryset = queryset.filter(date__gte=validated.get("from_date"))
        if validated.get("to_date"):
            queryset = queryset.filter(date__lte=validated.get("to_date"))
        
        print("Ordering Info:", validated.get("order"))  # Debugging line
        order_info = validated.get("order", [])

        total_count = queryset.count()

        # Manual Pagination for DataTables
        start = validated.get("start", 0)
        length = validated.get("length", 10)
        

        print("Pagination - start:", start, "length:", length)  # Debugging line

        if length != -1:
            paginated = list(queryset[start:start + length])
            # Get total count from a separate count query only if needed
            total_count = queryset.count() if start > 0 or len(paginated) == length else len(paginated)
        else:
            paginated = list(queryset)
            total_count = len(paginated)
        

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
SalesDealViewset_edit_reference_number = SalesDealViewSet.as_view({'post': 'clone_deal_with_new_ref'})




 
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
    reciepts1_used = sales_deal.receipt_id if sales_deal.receipt_id else ""
    reciepts2_used = sales_deal.receipt_id2 if sales_deal.receipt_id2 else ""      
    reciepts3_used = sales_deal.receipt_id3 if sales_deal.receipt_id3 else ""
    reciepts4_used = sales_deal.receipt_id4 if sales_deal.receipt_id4 else ""
    reciepts5_used = sales_deal.receipt_id5 if sales_deal.receipt_id5 else ""




    used_receipt_ids = [rid for rid in [reciepts1_used, reciepts2_used, reciepts3_used, reciepts4_used, reciepts5_used] if rid]
    print("Used Receipt IDs:", used_receipt_ids)

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

    sales_data = {
        'agents': agents,
        'receipts': receipts
    }

    return render(request, 'home/editsalesdeal.html', {'deal_id': pk, 'aws_url': aws_url, 'reference_number': sales_deal.reference_number ,'sales_data': json.dumps(sales_data)})






 

























