import re
from django import template
from django.contrib.auth.models import Group
from django.utils.safestring import mark_safe
from django.conf import settings
from datetime import date


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
def render_file_links(file_string):
    """
    Renders HTML <a> links for each file in a comma-separated full URL list.
    Extracts the label as the prefix before digits in the filename.
    Cleans S3 path by removing /live/classic_properties/.
    """
    if not file_string:
        return ""

    files = [f.strip() for f in file_string.split(",") if f.strip()]
    output = []

    for index, file_url in enumerate(files, start=1):

        # 🔥 REMOVE unwanted path segment
        file_url = re.sub(r'/live/classic_properties/', '/', file_url)

        # extract filename after "rental/"
        filename = file_url.split("rental")[-1]

        # extract label before digits
        match = re.search(r'([a-zA-Z_]+)\d+', filename)
        label = match.group(1) if match else filename

        html = f'<div class="upload_prev"><a href="{file_url}" target="_blank">{label} {index}</a></div>'
        output.append(html)

    return mark_safe("\n".join(output))


@register.filter
def clean_s3(url):
    """Removes /live/<tenant>/ from S3 URLs."""
    if not url:
        return url
    return re.sub(r'/live/[^/]+/', '/live/', url)



@register.filter
def split(value, key):
    """Splits the string by the given key."""
    return value.split(key)

@register.filter
def get_user_groups(user):
    """Returns a list of group names the user belongs to."""
    return [group.name for group in user.groups.all()]



def your_view(request):
    ...
    context = {
        'today': date.today()
    }
    ...


# in your_app/templatetags/custom_tags.py


# register = template.Library()

@register.filter
def split_commas(value):
    """
    Split a comma-separated string into a list of trimmed items.
    Returns empty list if value is falsy.
    """
    if not value:
        return []
    # value may already be a list; handle that
    if isinstance(value, (list, tuple)):
        return [str(v).strip() for v in value if v]
    return [s.strip() for s in str(value).split(',') if s.strip()]



 