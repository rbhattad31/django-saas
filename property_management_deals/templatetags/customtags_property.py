from django import template
from django.contrib.auth.models import Group
from django.utils.safestring import mark_safe
import re

register = template.Library()
 
# use this in the sidenav.html
@register.filter(name='has_group')
def has_group(user, group_name):
    result = user.groups.filter(name=group_name).exists()
    print(f"[has_group] Checking if user '{user}' is in group '{group_name}': {result}")  # Debug
    return result
@register.filter(name='get_user_groups')
def get_user_groups(user):
    print(f"Getting groups for user: {user}, groups: {user.groups.all()}")  # Debug
    return user.groups.values_list('name', flat=True)


print("Module loaded successfully")


#render file links function is for 
@register.simple_tag
def render_file_links(file_string, base_url="", reference_number=""):
    """
    Generates HTML links for a comma-separated list of filenames.
    Shows only the prefix + counter as label.
    """
    print(file_string)
    print(base_url)
    print("reference number: ", reference_number)
    if not file_string:
        return ""
 
    files = [f.strip() for f in file_string.split(",") if f.strip()]
    output = []
 
    for index, file in enumerate(files, start=1):
        # Extract prefix from filename
        match = re.match(r'^([a-zA-Z_]+)\d+', file)
        label = match.group(1) if match else file
 
        # Build full URL
        file_url = f"{base_url}{reference_number}/{file}"
        html = f'<div class="upload_prev"><a href="{file_url}" target="_blank">{label} {index}</a></div>'
        output.append(html)
 
    return mark_safe("\n".join(output))   
 