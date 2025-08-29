from django.core.cache import cache

# Check what's in cache for your user
user_id = 1  # Replace with your user ID
cache_key = f"user_perms:{user_id}"
perms = cache.get(cache_key, [])
print(f"Cached permissions: {perms}")
print(f"Has view_all_rental_deals: {'core.view_all_rental_deals' in perms}")

# Check if cache is empty
if not perms:
    print("❌ Cache is empty - user needs to login again")