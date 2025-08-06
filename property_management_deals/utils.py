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
    saved_path = storage.save(f"{url}", ContentFile(file_obj.read()))
    print("File uploaded to S3:", saved_path)  # Debugging line to confirm upload

    return saved_path

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
    if storage.exists(file_path):
        storage.delete(file_path)
        print(f"Deleted: {file_path}")
        return True
    else:
        print(f"File not found: {file_path}")
        return False