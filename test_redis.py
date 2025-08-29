import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_saas.settings')
django.setup()

from django.core.cache import cache

# Test Redis connection
try:
    cache.set('test_key', 'test_value', 30)
    value = cache.get('test_key')
    if value == 'test_value':
        print("✅ Redis is working!")
    else:
        print("❌ Redis not working - value mismatch")
except Exception as e:
    print(f"❌ Redis connection failed: {e}")