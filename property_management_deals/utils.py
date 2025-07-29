from urllib.parse import urlparse
# from botocore.exceptions import NoCredentialsError
# from botocore import exception
import time
import os
import re
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

def upload_file_to_full_s3_url(file_obj, url):
    saved_path = default_storage.save(f"{url}", ContentFile(file_obj.read()))

    return saved_path

def delete_from_s3(file_path):
    """
    Deletes a file from the media folder.

    :param file_path: Relative path from MEDIA_ROOT (e.g., 'rental/docs/file.jpg')
    :return: True if deleted, False if file doesn't exist
    """
    file_path = os.path.normpath(file_path.lstrip('/'))
    full_path = os.path.join(settings.MEDIA_ROOT, file_path)

    if os.path.isfile(full_path):
        try:
            os.remove(full_path)
            print(f"Deleted: {full_path}")
            return True
        except Exception as e:
            print(f"Error deleting {full_path}: {e}")
            return False
    else:
        print(f"File not found: {full_path}")
        return False
 