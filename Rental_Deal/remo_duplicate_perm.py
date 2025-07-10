from django.contrib.auth.models import Permission

# Find and delete all permissions with incorrect codename pattern
duplicates = Permission.objects.filter(codename__icontains='rentaldeal').exclude(codename__icontains='rental_deals')

duplicates_count = duplicates.count()
print(f"Found {duplicates_count} duplicate permissions:")

for p in duplicates:
    print(f"- {p.codename}")

# Safe to delete after confirming
duplicates.delete()
print("Deleted duplicate permissions.")