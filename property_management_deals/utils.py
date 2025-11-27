# from urllib.parse import urlparse
# # from botocore.exceptions import NoCredentialsError
# # from botocore import exception
# import time
# import os
# import re
# from django.conf import settings
# from django.core.files.base import ContentFile
# # from django.core.files.storage import  get_storage_class
# from django.utils.module_loading import import_string
# # print("UTILS STORAGE INIT:", type(get_storage_class()))


# # # rental/utils.py
# # # these 4 header files are newly written for verifying the filepaths are there or not in aws s3. 
# # from django.conf import settings
# # from django.utils.module_loading import import_string
# # from rest_framework.response import Response
# # from rest_framework import status
# # #we added above 4 headers newly for files verification




# def upload_file_to_full_s3_url(file_obj, url):
#     storage_class = import_string(settings.DEFAULT_FILE_STORAGE)
#     storage = storage_class()

#     base_url = settings.AWS_URL.replace('/classic_properties', '').rstrip('/')

#     # Build full S3 key for saving
#     # storage.save works with paths relative to bucket, but for clarity, prepend "live/"
#     s3_key = f"live/{url.lstrip('/')}"

#     # Upload file to S3
#     saved_path = storage.save(s3_key, ContentFile(file_obj.read()))

#     # Build full URL including domain for debugging or logging
#     full_s3_url = f"{base_url}/{saved_path[len('live/'):]}".rstrip('/')

#     # Return only relative path starting with /
#     cleaned_path = '/' + saved_path[len('live/'):].lstrip('/')

#     print("✅ File uploaded to S3 key:", saved_path)
#     print("✅ Full S3 URL:", full_s3_url)
#     print("✅ Returning cleaned path:", cleaned_path)

#     return cleaned_path





# # # adding new functions for verification of file paths


# # def build_full_s3_url(relative_path: str) -> str:
# #     """
# #     Convert '/rental/.../file.pdf' -> '<AWS_URL>/live/rental/.../file.pdf'
# #     Use settings.AWS_URL which you already use in upload_file_to_full_s3_url.
# #     """
# #     if not relative_path:
# #         return ""
# #     base_url = settings.AWS_URL.rstrip('/')  # e.g. https://your-bucket.s3.amazonaws.com
# #     cleaned = relative_path.lstrip('/')      # remove leading slash
# #     # keep same 'live/' prefix convention used by upload_file_to_full_s3_url
# #     return f"{base_url}/live/{cleaned}"


# # def _normalize_path_to_s3_key(path):
# #     if not path:
# #         return None
# #     cleaned = str(path).strip().lstrip('/')
# #     return f"live/{cleaned}" if cleaned else None

# # def _split_paths(value):
# #     """Return list of trimmed paths from string (comma-separated) or list/tuple."""
# #     if value is None:
# #         return []
# #     if isinstance(value, (list, tuple)):
# #         items = []
# #         for v in value:
# #             if not v:
# #                 continue
# #             if isinstance(v, str) and ',' in v:
# #                 items += [p.strip() for p in v.split(',') if p.strip()]
# #             else:
# #                 items.append(str(v).strip())
# #         return items
# #     if isinstance(value, str):
# #         return [p.strip() for p in value.split(',') if p.strip()]
# #     return [str(value).strip()]

# # def verify_or_raise_s3_errors(data: dict, file_fields: list):
# #     """
# #     If any referenced file path is missing in S3, return a DRF Response(400)
# #     containing the field -> list of missing paths. If OK, return None.
# #     """
# #     storage = import_string(settings.DEFAULT_FILE_STORAGE)()
# #     missing_files = {}

# #     for field in file_fields:
# #         raw_value = data.get(field)
# #         paths = _split_paths(raw_value)
# #         if not paths:
# #             continue

# #         missing = []
# #         for p in paths:
# #             s3_key = _normalize_path_to_s3_key(p)
# #             try:
# #                 exists = bool(s3_key and storage.exists(s3_key))
# #             except Exception as e:
# #                 # treat storage errors as missing
# #                 print(f"verify_or_raise_s3_errors: storage.exists() error for {s3_key}: {e}")
# #                 exists = False

# #             if not exists:
# #                 missing.append(p)

# #         if missing:
# #             missing_files[field] = missing

# #     if missing_files:
# #         return Response(
# #             {
# #                 "success": False,
# #                 "message": "Some uploaded files are missing in S3.",
# #                 "missing_files": missing_files,
# #             },
# #             status=status.HTTP_400_BAD_REQUEST,
# #         )

# #     return None
# #_normalize_path_to_s3_key,_split_paths,verify_or_raise_s3_errors,build_full_s3_url these are the new 4 functions which i added.

# def delete_from_s3(file_path):
#     """
#     Deletes a file from the media folder.

#     :param file_path: Relative path from MEDIA_ROOT (e.g., 'rental/docs/file.jpg')
#     :return: True if deleted, False if file doesn't exist
#     """
#     file_path = os.path.normpath(file_path.lstrip('/'))
#     full_path = os.path.join(settings.MEDIA_LOCATION, file_path)
#     storage_class = import_string(settings.DEFAULT_FILE_STORAGE)
#     storage = storage_class()

#     s3_key = f"live/{file_path}"

#     if storage.exists(s3_key):
#         storage.delete(s3_key)
#         print(f"Deleted: {s3_key}")
#         return True
#     else:
#         print(f"File not found: {s3_key}")
#         return False
#---------------------------------------------------------------------------------------

# from urllib.parse import urlparse
# # from botocore.exceptions import NoCredentialsError
# # from botocore import exception
# import time
# import os
# import re
# from django.conf import settings
# from django.core.files.base import ContentFile
# # from django.core.files.storage import  get_storage_class
# from django.utils.module_loading import import_string
# # print("UTILS STORAGE INIT:", type(get_storage_class()))
 
# def upload_file_to_full_s3_url(file_obj, url):
#     storage_class = import_string(settings.DEFAULT_FILE_STORAGE)
#     storage = storage_class()
 
#     base_url = settings.AWS_URL.replace('/classic_properties', '').rstrip('/')
 
#     # Build full S3 key for saving
#     # storage.save works with paths relative to bucket, but for clarity, prepend "live/"
#     s3_key = f"live/{url.lstrip('/')}"
 
#     # Upload file to S3
#     saved_path = storage.save(s3_key, ContentFile(file_obj.read()))
 
#     # Build full URL including domain for debugging or logging
#     full_s3_url = f"{base_url}/{saved_path[len('live/'):]}".rstrip('/')
 
#     # Return only relative path starting with /
#     cleaned_path = '/' + saved_path[len('live/'):].lstrip('/')
 
#     print("✅ File uploaded to S3 key:", saved_path)
#     print("✅ Full S3 URL:", full_s3_url)
#     print("✅ Returning cleaned path:", cleaned_path)
 
#     return cleaned_path
 
# def delete_from_s3(file_path):
#     """
#     Deletes a file from the media folder.
 
#     :param file_path: Relative path from MEDIA_ROOT (e.g., 'rental/docs/file.jpg')
#     :return: True if deleted, False if file doesn't exist
#     """
#     file_path = os.path.normpath(file_path.lstrip('/'))
#     full_path = os.path.join(settings.MEDIA_LOCATION, file_path)
#     storage_class = import_string(settings.DEFAULT_FILE_STORAGE)
#     storage = storage_class()
 
#     s3_key = f"live/{file_path}"
 
#     if storage.exists(s3_key):
#         storage.delete(s3_key)
#         print(f"Deleted: {s3_key}")
#         return True
#     else:
#         print(f"File not found: {s3_key}")
#         return False
   
 
 
# def s3_file_exists(filepath):
#     storage_class = import_string(settings.DEFAULT_FILE_STORAGE)
#     storage = storage_class()
#     try:
#         print(f"Checking existence for {filepath}")
#         url = f"/live{filepath}"
#         is_present =  storage.exists(url)
#         print(f"Checked existence for {filepath}: {is_present}")
#         return is_present
#     except Exception as e:
#         print(f"S3 existence check failed for {filepath}: {e}")
#         return False

#----------------------------------------------------------------------------
# rental/utils.py - robust S3 helpers (drop-in replacement)

import os
import time
from django.conf import settings
from django.core.files.base import ContentFile
from django.utils.module_loading import import_string
import boto3
from botocore.exceptions import ClientError, NoCredentialsError, EndpointConnectionError
import re
from urllib.parse import quote 
from urllib.parse import urlparse


def _normalize_public_url(raw_url):
    """
    Normalize a URL-like string to a valid absolute URL starting with http(s)://
    Handles inputs like:
      - 'https:/cp-new.s3.amazonaws.com/...'  -> 'https://cp-new.s3.amazonaws.com/...'
      - 'https//cp-new.s3.amazonaws.com/...'  -> 'https://cp-new.s3.amazonaws.com/...'
      - '//cp-new.s3.amazonaws.com/...'       -> 'https://cp-new.s3.amazonaws.com/...'
      - 'cp-new.s3.amazonaws.com/...'         -> 'https://cp-new.s3.amazonaws.com/...'
      - already-correct values are returned unchanged
    """
    if not raw_url:
        return raw_url
    u = str(raw_url).strip()

    # Fix common typos first
    u = u.replace('https//', 'https://').replace('http//', 'http://')

    # If it starts with exactly one slash + host (//host/path), add https:
    if u.startswith('//'):
        u = 'https:' + u

    # If it looks like 'https:/something' (one slash), fix to 'https://'
    u = u.replace('https:/' , 'https://') if u.startswith('https:/') and not u.startswith('https://') else u
    u = u.replace('http:/' , 'http://') if u.startswith('http:/') and not u.startswith('http://') else u

    # If no scheme present at all, add https://
    parsed = urlparse(u)
    if not parsed.scheme:
        u = 'https://' + u.lstrip('/')

    return u

def _normalize_to_s3_key(raw_path):
    """
    Normalize DB path -> storage key.
    Input examples:
      '/rental/.../file.pdf'
      'rental/.../file.pdf'
      'live/rental/.../file.pdf'
    Output:
      'live/rental/.../file.pdf'
    """
    if not raw_path:
        return None
    p = str(raw_path).strip().lstrip('/')
    return p if p.startswith('live/') else f"live/{p}"

def get_storage():
    """Return Django storage instance from DEFAULT_FILE_STORAGE"""
    storage_class = import_string(settings.DEFAULT_FILE_STORAGE)
    return storage_class()

def get_boto3_client():
    """Return boto3 S3 client using env vars or settings (region detection)."""
    region = os.environ.get('AWS_DEFAULT_REGION') or getattr(settings, 'AWS_S3_REGION_NAME', None)
    return boto3.client(
        "s3",
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID') or getattr(settings, 'AWS_ACCESS_KEY_ID', None),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY') or getattr(settings, 'AWS_SECRET_ACCESS_KEY', None),
        region_name=region
    )

def test_s3_connection(bucket_name=None):
    """
    Test S3 connectivity and basic write/delete.
    Returns dict: {'connected': bool, 'bucket_ok': bool, 'write_ok': bool, 'message': str}
    """
    bucket = bucket_name or os.environ.get('AWS_BUCKET') or getattr(settings, 'AWS_STORAGE_BUCKET_NAME', None)
    if not bucket:
        return {"connected": False, "bucket_ok": False, "write_ok": False, "message": "No bucket configured"}

    client = get_boto3_client()
    test_key = f"live/s3_connection_test_{int(time.time())}.txt"

    # head_bucket
    try:
        client.head_bucket(Bucket=bucket)
    except NoCredentialsError:
        return {"connected": False, "bucket_ok": False, "write_ok": False, "message": "No AWS credentials found"}
    except EndpointConnectionError as e:
        return {"connected": False, "bucket_ok": False, "write_ok": False, "message": f"Endpoint error: {e}"}
    except ClientError as e:
        return {"connected": True, "bucket_ok": False, "write_ok": False, "message": f"head_bucket error: {e}"}

    # put/get/delete
    try:
        client.put_object(Bucket=bucket, Key=test_key, Body=b"ok")
        resp = client.get_object(Bucket=bucket, Key=test_key)
        body = resp['Body'].read()
        client.delete_object(Bucket=bucket, Key=test_key)
        if body == b"ok":
            return {"connected": True, "bucket_ok": True, "write_ok": True, "message": "S3 connected and writable"}
        else:
            return {"connected": True, "bucket_ok": True, "write_ok": False, "message": "Write/read mismatch"}
    except ClientError as e:
        return {"connected": True, "bucket_ok": True, "write_ok": False, "message": f"put/get/delete error: {e}"}
    except Exception as e:
        return {"connected": False, "bucket_ok": False, "write_ok": False, "message": str(e)}

def s3_file_exists(db_path, bucket_name=None):
    """
    Check if db_path exists in S3.
    db_path examples: '/rental/.../file.pdf' or 'rental/.../file.pdf'
    Returns True if exists, False otherwise (prints status).
    """
    if not db_path:
        print("s3_file_exists: empty path")
        return False

    bucket = bucket_name or os.environ.get('AWS_BUCKET') or getattr(settings, 'AWS_STORAGE_BUCKET_NAME', None)
    if not bucket:
        print("s3_file_exists: no bucket configured")
        return False

    s3_key = _normalize_to_s3_key(db_path)
    client = get_boto3_client()
    try:
        client.head_object(Bucket=bucket, Key=s3_key)
        print(f"✅ Exists in S3: {s3_key}")
        return True
    except ClientError as e:
        code = e.response.get("Error", {}).get("Code", "")
        if code in ("404", "NoSuchKey"):
            print(f"❌ NOT found in S3: {s3_key}")
        elif code in ("403", "AccessDenied"):
            print(f"⚠️ ACCESS DENIED for: {s3_key}")
        else:
            print(f"❌ head_object error for {s3_key}: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error when checking {s3_key}: {e}")
        return False

# def upload_file_to_full_s3_url(file_obj, db_desired_path):
#     """
#     Upload a file using Django storage and return the DB-friendly path (leading slash, without 'live/').
#     - file_obj: file-like object (UploadedFile)
#     - db_desired_path: '/rental/.../filename.pdf'
#     """
#     storage = get_storage()
#     s3_key = _normalize_to_s3_key(db_desired_path)
#     if not s3_key:
#         print("upload_file_to_s3_and_return_dbpath: invalid desired path")
#         return None

#     try:
#         saved_path = storage.save(s3_key, ContentFile(file_obj.read()))
#         normalized = saved_path.lstrip('/')
#         db_path = '/' + (normalized[len('live/'):] if normalized.startswith('live/') else normalized)
#         try:
#             public_url = storage.url(normalized)
#         except Exception:
#             public_url = None
#         # print("Uploaded -> saved_path:", saved_path)
#         # print("Public URL (storage.url) ->", public_url)
#         # print("Return DB path ->", db_path)


#         # Debug prints to help diagnose domain issues
#         print("Uploaded -> saved_path:", saved_path)
#         print("storage type:", type(storage))
#         print("storage.bucket_name:", getattr(storage, 'bucket_name', None))
#         print("storage.custom_domain:", getattr(storage, 'custom_domain', None))
#         print("storage.base_url:", getattr(storage, 'base_url', None))
#         print("Public URL (storage.url) ->", public_url)
#         print("Return DB path ->", db_path)
#         return db_path
#     except Exception as e:
#         print("upload error:", e)
#         return None
import re
# def upload_file_to_full_s3_url(file_obj, db_desired_path):
#     """
#     Upload a file and return tuple: (db_path, public_url)
#     - db_desired_path: '/rental/.../filename.pdf'
#     """
#     storage = get_storage()
#     s3_key = _normalize_to_s3_key(db_desired_path)
#     if not s3_key:
#         print("upload_file_to_s3_and_return_dbpath: invalid desired path")
#         return None, None

#     # sanitize name in s3_key (optional): replace multiple spaces with single underscore
#     s3_key = re.sub(r"\s+", "_", s3_key)

#     try:
#         saved_path = storage.save(s3_key, ContentFile(file_obj.read()))
#         normalized = saved_path.lstrip('/')
#         db_path = '/' + (normalized[len('live/'):] if normalized.startswith('live/') else normalized)

#         # Try to get public URL from storage — storage.url expects the storage key (without leading '/')
#         try:
#             public_url = storage.url(normalized)
#         except Exception as e:
#             print("storage.url() failed:", e)
#             public_url = None

#         # If storage.url failed but you want public URL, try to build from settings.AWS_S3_CUSTOM_DOMAIN
#         if not public_url:
#             bucket_domain = getattr(settings, 'AWS_S3_CUSTOM_DOMAIN', None) or getattr(settings, 'AWS_URL', None)
#             if bucket_domain:
#                 # Ensure no double slashes
#                 public_url = f"{bucket_domain.rstrip('/')}/{normalized}"

#         # Make sure URL is safe (encode spaces etc)
#         if public_url:
#             public_url = quote(public_url, safe=':/?&=%#')

#         print("Uploaded -> saved_path:", saved_path)
#         print("Public URL (storage.url) ->", public_url)
#         print("Return DB path ->", db_path)
#         return db_path, public_url
#     except Exception as e:
#         print("upload error:", e)
#         return None, None



def upload_file_to_full_s3_url(file_obj, db_desired_path):
    """
    Upload a file and return tuple: (db_path, public_url)
    - db_desired_path expected like '/rental/.../filename.pdf'
    - public_url will be an absolute URL (or None if it couldn't be determined).
    """
    storage = get_storage()
    # Normalize to 'live/...' key
    s3_key = _normalize_to_s3_key(db_desired_path)
    if not s3_key:
        print("upload_file_to_s3_and_return_dbpath: invalid desired path")
        return None, None

    # sanitize spaces and repeated whitespace in the S3 key
    s3_key = re.sub(r"\s+", "_", s3_key)

    try:
        # Save using Django storage. saved_path is the key that storage uses to reference the object.
        saved_path = storage.save(s3_key, ContentFile(file_obj.read()))
        # normalized_saved is what we'll store in DB (strip any leading '/')
        normalized_saved = saved_path.lstrip('/')

        # db_path: what you store in your DB (keep previous 'no-live/' behaviour)
        db_path = '/' + (normalized_saved[len('live/'):] if normalized_saved.startswith('live/') else normalized_saved)

        public_url = None

        # Preferred: ask storage for the URL (Django-storages S3 backend implements url())
        try:
            # Pass the storage key exactly as saved (no added leading slash)
            public_url = storage.url(normalized_saved)
        except Exception as e:
            # storage.url() may fail for private buckets or custom backends; continue to try other methods
            print("storage.url() failed:", e)
            public_url = None

        # Fallback: build from AWS_S3_CUSTOM_DOMAIN or AWS_URL (if present)
        # if not public_url:
        #     bucket_domain = getattr(settings, 'AWS_S3_CUSTOM_DOMAIN', None) or getattr(settings, 'AWS_URL', None)
        #     if bucket_domain:
        #         # Ensure no trailing slash on bucket_domain, encode only the path portion
        #         # If storage saved key includes 'live/', keep it in the path used in URL building.
        #         encoded_path = quote(normalized_saved, safe="/:@")  # preserve slashes and common safe chars
        #         public_url = f"{bucket_domain.rstrip('/')}/{encoded_path}"

        if not public_url:
            bucket_domain = getattr(settings, 'AWS_S3_CUSTOM_DOMAIN', None) or getattr(settings, 'AWS_URL', None)
            if bucket_domain:
                # Normalize common mis-forms and ensure a single valid scheme (https://)
                bd = str(bucket_domain).strip()
                # fix common typos like 'https//host' or 'http//host'
                bd = bd.replace('https//', 'https://').replace('http//', 'http://')
                # remove accidental leading slashes
                bd = bd.lstrip('/')
                # if scheme missing, default to https
                if not (bd.startswith('http://') or bd.startswith('https://')):
                    bd = 'https://' + bd
                # Ensure no trailing slash before joining with path
                bd = bd.rstrip('/')

                # encode only the path portion (normalized_saved already contains 'live/...' if applicable)
                encoded_path = quote(normalized_saved, safe="/:@")
                public_url = f"{bd}/{encoded_path}"

        # Final safety: ensure public_url looks like an absolute URL (has scheme)
        # if public_url and not public_url.startswith("http"):
        #     # If bucket_domain was set but missing scheme, try to add https://
        #     public_url = "https://" + public_url.lstrip('/')
        if public_url and not (public_url.startswith("http://") or public_url.startswith("https://")):
           public_url = "https://" + public_url.lstrip('/')


        # Debug prints
        print("Uploaded -> saved_path:", saved_path)
        print("storage type:", type(storage))
        print("storage.bucket_name:", getattr(storage, 'bucket_name', None))
        print("storage.custom_domain:", getattr(storage, 'custom_domain', None))
        print("storage.base_url:", getattr(storage, 'base_url', None))
        print("Public URL (storage.url) ->", public_url)
        print("Return DB path ->", db_path)

        return db_path, public_url
    except Exception as e:
        print("upload error:", e)
        return None, None



def delete_from_s3(db_path):
    """
    Delete object from S3 given DB path (returns True if deleted).
    """
    bucket = os.environ.get('AWS_BUCKET') or getattr(settings, 'AWS_STORAGE_BUCKET_NAME', None)
    if not bucket:
        print("delete_from_s3: no bucket configured")
        return False
    s3_key = _normalize_to_s3_key(db_path)
    client = get_boto3_client()
    try:
        client.delete_object(Bucket=bucket, Key=s3_key)
        print("Deleted (or didn't exist):", s3_key)
        return True
    except ClientError as e:
        print("delete_from_s3 error:", e)
        return False
    except Exception as e:
        print("delete_from_s3 unexpected error:", e)
        return False


