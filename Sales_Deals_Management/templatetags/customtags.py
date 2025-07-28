import os
import re
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def render_file_links(file_string, base_url="", reference_number=""):
    """
    Generates HTML links for a comma-separated list of filenames.
    Uses the filename prefix as label, removing the timestamp and extension.
    """
    if not file_string:
        return ""

    files = [f.strip() for f in file_string.split(",") if f.strip()]
    output = []

    for index, file in enumerate(files, start=1):
        # Remove file extension
        file_base = os.path.splitext(file)[0]  # e.g., 'owners_passport_copy_3996351241537533482'

        # Extract label by removing the last numeric suffix
        label = re.sub(r'_\d{10,}$', '', file_base)  # removes _ + 10+ digit timestamp

        # Optional: make label more human readable
        label = label.replace('_', ' ').title()  # 'owners_passport_copy' → 'Owners Passport Copy'

        # Build full URL
        file_url = f"{base_url}{reference_number}/{file}"
        html = f'<div class="upload_prev"><a href="{file_url}" target="_blank">{label} {index}</a></div>'
        output.append(html)

    return mark_safe("\n".join(output))
