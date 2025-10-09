from urllib.parse import urlparse
# from botocore.exceptions import NoCredentialsError
# from botocore import exception
import time
import os
import re
from django.conf import settings
from django.core.files.base import ContentFile
# from django.core.files.storage import  get_storage_class
from django.utils.module_loading import import_string
# print("UTILS STORAGE INIT:", type(get_storage_class()))

def upload_file_to_full_s3_url(file_obj, url):
    storage_class = import_string(settings.DEFAULT_FILE_STORAGE)
    storage = storage_class()

    base_url = settings.AWS_URL.replace('/classic_properties', '').rstrip('/')

    # Build full S3 key for saving
    # storage.save works with paths relative to bucket, but for clarity, prepend "live/"
    s3_key = f"live/{url.lstrip('/')}"

    # Upload file to S3
    saved_path = storage.save(s3_key, ContentFile(file_obj.read()))

    # Build full URL including domain for debugging or logging
    full_s3_url = f"{base_url}/{saved_path[len('live/'):]}".rstrip('/')

    # Return only relative path starting with /
    cleaned_path = '/' + saved_path[len('live/'):].lstrip('/')

    print("✅ File uploaded to S3 key:", saved_path)
    print("✅ Full S3 URL:", full_s3_url)
    print("✅ Returning cleaned path:", cleaned_path)

    return cleaned_path

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

    s3_key = f"live/{file_path}"

    if storage.exists(s3_key):
        storage.delete(s3_key)
        print(f"Deleted: {s3_key}")
        return True
    else:
        print(f"File not found: {s3_key}")
        return False