import logging
import boto3
import csv
import os
from datetime import datetime

from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils import timezone
from django.core.mail import EmailMessage

from dateutil.relativedelta import relativedelta
from openpyxl import Workbook

from core.models import RentalDeals, SalesDeals
from Rental_Deal.Utilities import s3_file_exists
from django.template.loader import render_to_string


logger = logging.getLogger('Rental_Deal_File_Check.log')





from collections import defaultdict
import csv

# =====================================================
#  Grouping Helpers
# =====================================================

def group_missing_by_reference(csv_path):
    """
    Reads CSV and groups ERROR rows by Reference Number
    """
    grouped = defaultdict(list)

    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            # Only real missing files
            # if row.get("Severity") != "ERROR":
            #     continue

            reference = row.get("Reference_Number")

            if not reference:
                continue

            grouped[reference].append(row)

    return grouped



# =====================================================
# S3 HELPERS (WITH LOGS)
# =====================================================

def s3_file_exists_in_versions(key):
    """
    Check file in main bucket versions
    """
    s3 = boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME,
    )

    try:
        paginator = s3.get_paginator("list_object_versions")
        # Optimization: Use Prefix=key but verify exact match
        for page in paginator.paginate(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Prefix="live/classic_properties/"+key):
            
            # Check for Delete Markers FIRST (to identify if it's "deleted")
            for marker in page.get("DeleteMarkers", []):
                if marker["Key"] == "live/classic_properties/"+key and marker.get("IsLatest"):
                    logger.warning("FILE IS DELETED (Delete Marker is Latest) | key=%s", key)
                    print("FILE IS DELETED (Delete Marker is Latest) | key=%s", "live/classic_properties/"+key)
                    return True, marker["VersionId"], "DELETED"

            # Check for Active Versions
            for version in page.get("Versions", []):
                if version["Key"] == "live/classic_properties/"+key and version.get("IsLatest"):
                    logger.info("FILE IS ACTIVE | key=%s | version=%s", key, version["VersionId"])
                    print("FILE IS ACTIVE | key=%s | version=%s", "live/classic_properties/"+key, version["VersionId"])
                    return True, version["VersionId"], "ACTIVE"
            
            # If you just want to know if it EVER existed:
            for version in page.get("Versions", []):
                if version["Key"] == key:
                     return True, version["VersionId"], "ARCHIVED_VERSION"

        return False, None, "NOT_FOUND"

    except s3.exceptions.NoSuchBucket:
        logger.error("Bucket does not exist.")
    except Exception as e:
        logger.exception("Error checking versions: %s", e)
    return False, None, "ERROR"

def s3_file_exists_in_backup_bucket(key):
    """
    Check file in backup bucket
    """
    s3 = boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME,
    )
    key = "live/classic_properties/" + key
    print("Checking BACKUP bucket for key:", key)

    try:
        s3.head_object(Bucket="cproperties-deals-bkp", Key=key)
        logger.warning("FOUND IN BACKUP BUCKET: %s", key)
        return True

    except s3.exceptions.ClientError:
        logger.info("Not found in backup bucket: %s", key)
        return False


def s3_file_exists_in_backup_bucket_versions(key):
    """
    Check file in backup bucket versions
    """
    s3 = boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME,
    )

    try:
        key = "live/classic_properties/" + key
        logger.info("Checking BACKUP bucket versions for key: %s", key)
        paginator = s3.get_paginator("list_object_versions")
        for page in paginator.paginate(
            Bucket="cproperties-deals-bkp",
            Prefix=key
        ):
            for version in page.get("Versions", []):
                if version["Key"] == key:
                    logger.warning(
                        "FOUND IN BACKUP VERSION | key=%s | version=%s",
                        key, version["VersionId"]
                    )
                    return True, version["VersionId"]

            for marker in page.get("DeleteMarkers", []):
                if marker["Key"] == key:
                    logger.warning(
                        "BACKUP DELETE MARKER | key=%s | version=%s",
                        key, marker["VersionId"]
                    )
                    return True, marker["VersionId"]

        logger.error("NOT FOUND IN BACKUP VERSIONS: %s", key)
        return False, None

    except Exception:
        logger.exception("ERROR checking BACKUP versions for %s", key)
        return False, None


# =====================================================
# EMAIL (WITH LOGS)
# =====================================================

def send_missing_files_email(missing_count, preview, csv_path, excel_path):
    logger.info("Preparing email alert for %s missing files", missing_count)

    subject = f"[ALERT] Missing Rental Deal Files ({missing_count})"

    body = [
        f"Total Missing Files: {missing_count}",
        "",
        "Sample missing entries:",
    ]

    for item in preview:
        body.append(
            f"- Deal {item['deal_id']} ({item['reference']}) | "
            f"{item['field']} | {item['file']}"
        )

    body.append("")
    body.append("Please check attached CSV & Excel reports.")

    email = EmailMessage(
        subject=subject,
        body="\n".join(body),
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[admin[1] for admin in settings.ADMINS],
    )

    email.attach_file(csv_path)
    email.attach_file(excel_path)

    email.send(fail_silently=False)
    logger.warning("Missing files email sent successfully")


# get csv report path

def get_report_csv_path(module_name: str, prefix="missing_files"):
    """
    Returns CSV path like:
    reports/<module_name>/missing_files_YYYYMMDD_HHMMSS.csv
    """
    base_dir = os.path.join("reports", module_name)
    os.makedirs(base_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{prefix}_{timestamp}.csv"

    return os.path.join(base_dir, filename)




def send_grouped_missing_files_email(reference_number, missing_files):
    subject = f"[ALERT] Missing Rental Files | {reference_number}"

    html_body = render_to_string(
        "home/email_missing.html",
        {
            "reference_number": reference_number,
            "missing_files": missing_files,
        }
    )

    email = EmailMessage(
        subject=subject,
        body=html_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[admin[1] for admin in settings.ADMINS],
    )

    email.content_subtype = "html"
    email.send(fail_silently=False)











# =====================================================
# COMMAND
# =====================================================

class Command(BaseCommand):
    help = "Check RentalDeal files in S3 (streaming CSV, logs enabled)"

    def add_arguments(self, parser):
        parser.add_argument('--reference-number', type=str)
        parser.add_argument('--deal-id', type=int)
        parser.add_argument('--days', type=int)
        parser.add_argument('--months', type=int)

    def handle(self, *args, **options):

        logger.info("===== S3 FILE CHECK STARTED =====")

        file_fields = [
          'signed_mou',
            'new_title_deed',
            'old_title_deed',
            'owners_passport_copy',
            'buyers_passport_copy',
            'buyers_deposit_cheque_copy',
            'sellers_deposit_cheque_copy',
            'seller_poa_passport_copy',
            'buyer_poa_passport_copy',
            'owner_eid_copy',
            'buyer_eid_copy',
            'seller_poa_copy',
            'buyer_poa_copy',
            'buyer_poa_eid',
            'seller_poa_eid',
            'sale_kyc_number'
            'form_i_copy',
            'referral_agreement_copy',
            'management_approval_form_copy',
            'manager_cheque_copy',
            'screening',
        ]

        query = SalesDeals.objects.all().order_by("-id")

        if options.get('reference_number'):
            query = query.filter(reference_number=options['reference_number'])
            logger.info("Filtering by reference number")

        if options.get('deal_id'):
            query = query.filter(id=options['deal_id'])
            logger.info("Filtering by deal ID")

        now = timezone.now()

        if options.get('days'):
            query = query.filter(
                created_at__gte=now - timezone.timedelta(days=options['days'])
            )
            logger.info("Filtering last %s days", options['days'])

        if options.get('months'):
            query = query.filter(
                created_at__gte=now - relativedelta(months=options['months'])
            )
            logger.info("Filtering last %s months", options['months'])

        # ================= CSV STREAM =================

        os.makedirs("reports", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_path = get_report_csv_path("rental")

        fieldnames = [
    "Deal_ID",
    "Reference_Number",
    "Field",
    "File_Name",
    "S3_Original_versions",
    "S3_Backup",
    "S3_Backup_versions",
    "S3_Path",
    "Severity",
]

        csv_file = open(csv_path, "w", newline="", encoding="utf-8")
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        csv_writer.writeheader()

        missing_count = 0
        version_count = 0
        email_preview = []
        total_checked = 0


        # ================= MAIN LOOP =================

        for rental in query:
            logger.info(
                "Checking Deal ID=%s Reference=%s",
                rental.id, rental.reference_number
            )

            for field in file_fields:
                value = getattr(rental, field, "")
                if not value:
                    continue

                for filename in [f.strip() for f in value.split(",") if f.strip()]:
                    total_checked += 1
                    s3_path = f"sale/referencenumber_CPS/{rental.reference_number}/{filename}"

                    logger.info("Checking file: %s", s3_path)

                    if s3_file_exists(s3_path):
                        logger.info("FOUND in main S3: %s", s3_path)
                        continue

                    found, version_id, status = s3_file_exists_in_versions(s3_path)

                    if found:
                        version_count += 1
                        csv_writer.writerow({
                            "Deal_ID": rental.id,
                            "Reference_Number": rental.reference_number,
                            "Field": field,
                            "File_Name": filename,
                            "S3_Original_versions": "YES" ,
                            "S3_Backup": "" ,
                            "S3_Backup_versions": "" ,

                            "S3_Path": s3_path,

                            "Severity": "WARNING" 
                        })
                        continue

                    if s3_file_exists_in_backup_bucket(s3_path):
                        version_count += 1
                        csv_writer.writerow({
                            "Deal_ID": rental.id,
                            "Reference_Number": rental.reference_number,    
                            "Field": field,
                            "File_Name": filename,
                            "S3_Original_versions": "" ,
                            "S3_Backup": "YES" ,
                            "S3_Backup_versions": "" ,

                            "S3_Path": s3_path,

                            "Severity": "WARNING" 
                        })
                        continue

                    if s3_file_exists_in_backup_bucket_versions(s3_path)[0]:
                        version_count += 1
                        csv_writer.writerow({
                            "Deal_ID": rental.id,
                            "Reference_Number": rental.reference_number,    
                            "Field": field,
                            "File_Name": filename,
                            "S3_Original_versions": "" ,
                            "S3_Backup": "" ,
                            "S3_Backup_versions": "YES" ,

                            "S3_Path": s3_path,

                            "Severity": "WARNING" 
                        })


                        continue

                    # ❌ REAL MISSING
                    missing_count += 1
                    csv_writer.writerow({
                        "Deal_ID": rental.id,
                        "Reference_Number": rental.reference_number,
                        "Field": field,
                        "File_Name": filename,
                        "S3_Original_versions": "NO" ,
                        "S3_Backup": "NO" , 
                        "S3_Backup_versions": "NO" ,

                        "S3_Path": s3_path,
                        "Severity": "ERROR",
                    })

                    logger.error(
                        "MISSING FILE | deal_id=%s reference=%s field=%s file=%s",
                        rental.id, rental.reference_number, field, filename
                    )

                    if len(email_preview) < 10:
                        email_preview.append({
                            "deal_id": rental.id,
                            "reference": rental.reference_number,
                            "field": field,
                            "file": filename
                        })

        csv_file.close()
        logger.info("CSV report written: %s", csv_path)

        # ================= EXCEL =================

        excel_path = csv_path.replace(".csv", ".xlsx")
        wb = Workbook()
        ws = wb.active
        ws.title = "Missing Files"

        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                ws.append(row)

        wb.save(excel_path)
        logger.info("Excel report created: %s", excel_path)

        # ================= SUMMARY =================

        logger.info(
            "CHECK COMPLETE | total_checked=%s missing=%s",
            total_checked, missing_count
        )

        self.stdout.write("=" * 60)
        self.stdout.write(f"Total files checked: {total_checked}")
        self.stdout.write(f"Missing files: {missing_count}")

        if missing_count > 0 or version_count > 0:
            print("thsisis  to check the grouped")
            grouped_items = group_missing_by_reference(csv_path=csv_path)
            print(grouped_items)
            for reference_number, items in grouped_items.items():
                print("Het Grouped Items ",reference_number , items)
                send_grouped_missing_files_email(
            reference_number=reference_number,
            missing_files=items
            )



            
            
            self.stdout.write(self.style.ERROR("Email alert sent"))
        else:
            self.stdout.write(self.style.SUCCESS("No missing files found"))

        logger.info("===== S3 FILE CHECK FINISHED =====")
