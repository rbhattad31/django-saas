
import json
import re
from django import template
from datetime import datetime
from django.utils.safestring import mark_safe

register = template.Library()


# use this in the sidenav.html
@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()



 

 
# used in  viewrentaldeal.html to serve files 
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





 

@register.filter
def ymd_to_dmy(value):
    """
    Converts 'YYYY-MM-DD' string to 'DD-MM-YYYY'.
    """
    try:
        print(value)
        return datetime.strptime(value, "%Y-%m-%d").strftime("%d-%m-%Y")
    except Exception:
        return value  # Fallback: return original if it fails




@register.simple_tag(takes_context=True)
def user_permissions_json(context):
    user = context['request'].user
    perms = list(user.get_all_permissions())  # convert set to list
    return mark_safe(json.dumps(perms))

@register.filter
def split_dmy(date_str, part):
    try:
        day, month, year = date_str.split("-")
        if part == "day":
            return day
        elif part == "month":
           
            return month  # Return full month name
        elif part == "year":
            return year
    except:
        return ""


# import re
# from django.utils.safestring import mark_safe

# def render_file_links_edit(file_string, base_url="", reference_number=""):
#     """
#     Generates HTML for a list of file links with remove buttons.
#     """
#     if not file_string:
#         return ""

#     files = [f.strip() for f in file_string.split(",") if f.strip()]
#     output = []

#     for index, file in enumerate(files, start=1):
#         # Extract label prefix
#         match = re.match(r'^([a-zA-Z_]+)\d+', file)
#         label = match.group(1) if match else file
#         display_name = f"{label} {index}"

#         # Build file URL
#         file_url = f"{base_url}{reference_number}/{file}"

#         html = f"""
#         <div class="files_list">
#             <a href="{file_url}" target="_blank">{display_name}</a>
#             <p class="remove_file"
#                id="{file}"
#                data-name="{label}"
#                data-existing="old"
#                style="cursor:pointer; display:inline-block; color:red; margin-left:10px;">
#                X
#             </p>
#         </div>
#         """
#         output.append(html)

#     return mark_safe("\n".join(output))
