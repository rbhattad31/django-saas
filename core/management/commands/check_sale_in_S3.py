import logging
import boto3

from django.core.management.base import BaseCommand
from django.conf import settings

from core.models import SalesDeals
from Rental_Deal.Utilities import s3_file_exists  # keep your existing import

logger = logging.getLogger('Sales_Deal_File_Check')


def s3_file_exists_in_versions(key):
    """
    Check if file exists in any S3 version.
    """
    s3 = boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME,
    )

    try:
        response = s3.list_object_versions(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME,
            Prefix=key,
        )
        print("checking sale module   the file  in versions  ")


        for version in response.get("Versions", []):
            if version["Key"] == key:
                return True, version["VersionId"]

        for marker in response.get("DeleteMarkers", []):
            if marker["Key"] == key:
                print( marker["Key"] , key)
                return True, marker["VersionId"]

        return False, None

    except Exception:
        logger.exception("Error checking S3 versions for %s", key)
        return False, None



def s3_file_exists_in_backup_bucket(key):
    """
    Check file existence in BACKUP S3 bucket.
    """
    s3 = boto3.client(
        "s3",
        aws_access_key_id= settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME,
    )
    print("checking the fiel in backup bucket ")

    try:
        s3.head_object(
            Bucket= "cproperties-deals-bkp",
            Key=key
        )
        return True

    except s3.exceptions.ClientError as e:
        if e.response["Error"]["Code"] == "404":
            return False




def s3_file_exists_in_backup_bucket_versions(key):
    s3 = boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME,
    )
    print("checking the fiel in backup bucket versions ")
    try:
        response = s3.list_object_versions(
            Bucket= "cproperties-deals-bkp",
            Prefix=key,
        )

        for version in response.get("Versions", []):
            if version["Key"] == key:
                return True, version["VersionId"]

        for marker in response.get("DeleteMarkers", []):
            if marker["Key"] == key:
                
                return True, marker["VersionId"]

        return False, None

    except Exception:
        logger.exception("Error checking backup bucket versions for %s", key)
        return False, None






class Command(BaseCommand):
    help = 'Check if all files in RentalDeals records exist in S3 bucket'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reference-number',
            type=str,
            help='Check files for a specific rental deal by reference number',
        )
        parser.add_argument(
            '--deal-id',
            type=int,
            help='Check files for a specific rental deal by ID',
        )

    def handle(self, *args, **options):

        file_fields = [
            'tenancy_contract',
            'owner_passport_copy',
            'tenant_passport_visa_copy',
            'tenant_emirates_id',
            'rental_deposit_cheque_copy',
            'title_deed',
            'owner_poa_pp_copy',
            'key_hand_over_form',
            'ejari',
            'owner_eid_copy',
            'poa_copy',
            'rental_kyc_number',
            'tenancy_application_form',
            'screening',
        ]

        query =  SalesDeals.objects.all().order_by("-id")

        if options.get('reference_number'):
            query = query.filter(reference_number=options['reference_number'])
            self.stdout.write(f"Checking reference: {options['reference_number']}")

        if options.get('deal_id'):
            query = query.filter(id=options['deal_id'])
            self.stdout.write(f"Checking deal ID: {options['deal_id']}")

        if not options.get('reference_number') and not options.get('deal_id'):
            self.stdout.write("Checking ALL rental deals...")

        missing_files = []
        found_files = []
        total_checked = 0

        for rental in query:
            self.stdout.write(
                f"\n--- Deal: {rental.reference_number} (ID: {rental.id}) ---"
            )

            for field_name in file_fields:
                field_value = getattr(rental, field_name, "")

                if not field_value or field_value.strip() == "":
                    continue

                file_names = [f.strip() for f in field_value.split(",") if f.strip()]

                for filename in file_names:
                    total_checked += 1
                    s3_path = f"sale/referencenumber_CPS/{rental.reference_number}/{filename}"
                    "live/classic_properties/sale/referencenumber_CPS/"
                    self.stdout.write(f"Checking S3 path: {s3_path}")

                    exists = s3_file_exists(s3_path)

                    # ✅ NORMAL FOUND
                    if exists:
                        found_files.append({
                            'deal_id': rental.id,
                            'reference': rental.reference_number,
                            'field': field_name,
                            'file': filename,
                            'path': s3_path
                        })
                        self.stdout.write(
                            self.style.SUCCESS(f"✓ {field_name}: {filename}")
                        )
                        continue

                    # 🔁 VERSION CHECK
                    version_exists, version_id = s3_file_exists_in_versions(s3_path)

                    if version_exists:
                        found_files.append({
                            'deal_id': rental.id,
                            'reference': rental.reference_number,
                            'field': field_name,
                            'file': filename,
                            'path': s3_path,
                            'version_id': version_id,
                        })

                        self.stdout.write(
                            self.style.WARNING(
                                f"⚠ Found in S3 versions: {field_name}: "
                                f"{filename} (version={version_id})"
                            )
                        )

                        logger.warning(
                            "File found in S3 versions: deal_id=%s reference=%s "
                            "field=%s file=%s version=%s",
                            rental.id, rental.reference_number,
                            field_name, filename, version_id
                        )
                        continue




                    backup_exists = s3_file_exists_in_backup_bucket(s3_path)

                    if backup_exists:
                        found_files.append({
                            'deal_id': rental.id,
                            'reference': rental.reference_number,
                            'field': field_name,
                            'file': filename,
                            'path': s3_path,
                            'bucket': 'backup'
                        })

                        self.stdout.write(
                            self.style.WARNING(
                                f"⚠ Found in BACKUP bucket: {field_name}: {filename}"
                            )
                        )

                        logger.warning(
                            "File found in BACKUP bucket: deal_id=%s reference=%s field=%s file=%s path=%s",
                            rental.id, rental.reference_number, field_name, filename, s3_path
                        )
                        continue


                    # 🔁 CHECK BACKUP BUCKET VERSIONS (OPTIONAL)
                    backup_version_exists, backup_version_id = s3_file_exists_in_backup_bucket_versions(s3_path)

                    if backup_version_exists:
                        found_files.append({
                            'deal_id': rental.id,
                            'reference': rental.reference_number,
                            'field': field_name,
                            'file': filename,
                            'path': s3_path,
                            'bucket': 'backup',
                            'version_id': backup_version_id
                        })

                        self.stdout.write(
                            self.style.WARNING(
                                f"⚠ Found in BACKUP bucket versions: {field_name}: "
                                f"{filename} (version={backup_version_id})"
                            )
                        )

                        logger.warning(
                            "File found in BACKUP bucket versions: deal_id=%s reference=%s "
                            "field=%s file=%s version=%s",
                            rental.id, rental.reference_number,
                            field_name, filename, backup_version_id
                        )
                        continue

                    # ❌ REALLY MISSING
                    missing_files.append({
                        'deal_id': rental.id,
                        'reference': rental.reference_number,
                        'field': field_name,
                        'file': filename,
                        'path': s3_path
                    })

                    self.stdout.write(
                        self.style.ERROR(f"✗ {field_name}: {filename}")
                    )

                    logger.error(
                        "Missing S3 file: deal_id=%s reference=%s field=%s "
                        "file=%s path=%s",
                        rental.id, rental.reference_number,
                        field_name, filename, s3_path
                    )

        # 📊 SUMMARY
        self.stdout.write("\n" + "=" * 60)
        self.stdout.write(f"Total files checked: {total_checked}")
        self.stdout.write(self.style.SUCCESS(f"Found: {len(found_files)}"))
        self.stdout.write(self.style.ERROR(f"Missing: {len(missing_files)}"))

        if missing_files:
            self.stdout.write("\n" + self.style.ERROR("MISSING FILES SUMMARY:"))
            for item in missing_files:
                self.stdout.write(
                    self.style.ERROR(
                        f"  Deal {item['deal_id']} ({item['reference']}) - "
                        f"{item['field']}: {item['file']}"
                    )
                )
            logger.error("Total missing files: %d", len(missing_files))
        else:
            self.stdout.write(self.style.SUCCESS("\nAll files present in S3!"))
            logger.info("All files verified in S3 successfully")
