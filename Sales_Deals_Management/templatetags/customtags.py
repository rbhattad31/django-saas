import os
import re
from django import template
from django.utils.safestring import mark_safe

register = template.Library()



@register.simple_tag
def render_file_links(file_string, base_url="", reference_number=""):
    """
    Generates HTML links for a comma-separated list of filenames.
    Uses the filename prefix (before the first numeric sequence) as label.
    """
    if not file_string:
        return ""

    files = [f.strip() for f in file_string.split(",") if f.strip()]
    output = []

    for index, file in enumerate(files, start=1):
        # Remove file extension
        file_base = os.path.splitext(file)[0]  # e.g., 'owners_passport_copy_4760838116'

        # Extract prefix before first number (e.g., "owners_passport_copy")
        match = re.match(r'^([a-zA-Z_]+)', file_base)
        label = match.group(1) if match else file_base

        # Make label more readable
        label = label.replace('_', ' ').title()

        # Build file URL
        file_url = f"{base_url}{reference_number}/{file}"
        html = f'<div class="upload_prev"><a href="{file_url}" target="_blank">{label} {index}</a></div>'
        output.append(html)

    return mark_safe("\n".join(output))

 