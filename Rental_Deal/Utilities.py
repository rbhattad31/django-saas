# import boto3
from urllib.parse import urlparse
# from botocore.exceptions import NoCredentialsError
# from botocore import exception
import time
import os
import re
from django.conf import settings
from django.core.files.base import ContentFile
# from django.core.files.storage import get_storage_class
from django.utils.module_loading import import_string
# print("UTILS STORAGE INIT:", type(get_storage_class()))
# print("UTILS STORAGE INIT:", )
from django.core.files.storage import default_storage

def upload_file_to_full_s3_url(file_obj, url):
    storage_class = import_string(settings.DEFAULT_FILE_STORAGE)
    storage = storage_class()
    print("Uploading file to S3 at URL:", url)
    saved_path = storage.save(f"live/classic_properties/{url}", ContentFile(file_obj.read()))

    print(f"Uploaded to: {saved_path}")

    files_is_presnet = storage.exists(f'{saved_path}')

    print(f"File exists after upload: {files_is_presnet}")

    if not files_is_presnet:
        return False
    else:
        return True

    

    

def delete_from_s3(file_path):
    """
    Deletes a file from the media folder.

    :param file_path: Relative path from MEDIA_ROOT (e.g., 'rental/docs/file.jpg')
    :return: True if deleted, False if file doesn't exist
    """
    file_path = os.path.normpath(file_path.lstrip('/'))
    full_path = os.path.join(settings.MEDIA_LOCATION, file_path)

    storage_class = import_string(settings.DEFAULT_FILE_STORAGE)

    storage = storage_class()
    if storage.exists(f'live/classic_properties/{file_path}'):
        storage.delete(f'live/classic_properties/{file_path}')
        print(f"Deleted: {f'live/classic_properties/{file_path}'}")
        return True
    else:
        print(f"File not found: {f'live/classic_properties/{file_path}'}")
        return False



def s3_file_exists(filepath):
    storage_class = import_string(settings.DEFAULT_FILE_STORAGE)
    storage = storage_class()
    try:
        print(f"Checking existence for {filepath}")
        url = f"/live/classic_properties/{filepath}"
        is_present =  storage.exists(url)
        print(f"Checked existence for {filepath}: {is_present}")
        return is_present
    except Exception as e:
        print(f"S3 existence check failed for {filepath}: {e}")
        return False



#     try:
#         # Parse the bucket name and key from the base URL
#         parsed_url = urlparse(base_s3_url)
#         domain_parts = parsed_url.netloc.split('.')
#         bucket = domain_parts[0]
#         region = domain_parts[2]
#         base_path = parsed_url.path.lstrip('/')  # Remove leading slash

#         # Final S3 key
#         full_s3_key = f"{base_path}"

#         # Initialize S3 client
#         s3 = boto3.client('s3', region_name=region)

#         # Upload file with public-read ACL
#         s3.upload_fileobj(
#             Fileobj=file_obj,
#             Bucket=bucket,
#             Key=full_s3_key,
#             ExtraArgs={'ACL': 'public-read'}
#         )

#         # Construct and return final URL
#         final_url = f"https://{bucket}.s3.{region}.amazonaws.com/{full_s3_key}"
#         return final_url

#     except Exception as e:
#         print(f"Error uploading file: {e}")
#         return None
    
# def delete_file_from_s3_url(file_url):
#     """
#     Delete a file from S3 using its full URL.

#     :param file_url: Full S3 file URL (e.g. https://bucket.s3.region.amazonaws.com/key)
#     :return: True if deleted, False otherwise
#     """
#     try:
#         # Parse the URL
#         parsed = urlparse(file_url)
#         netloc_parts = parsed.netloc.split('.')
#         bucket_name = netloc_parts[0]  # 'deal-saas'

#         # The key is everything after '.com/'
#         s3_key = parsed.path.lstrip('/')  # Remove leading slash

#         # Connect and delete
#         s3 = boto3.client('s3')
#         s3.delete_object(Bucket=bucket_name, Key=s3_key)

#         print(f"✅ Deleted: {s3_key} from bucket: {bucket_name}")
#         return True

#     except ClientError as e:
#         print(f"❌ AWS error: {e}")
#         return False
#     except Exception as e:
#         print(f"❌ Unexpected error: {e}")
#         return False

 