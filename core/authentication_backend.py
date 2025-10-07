# import bcrypt
# from django.contrib.auth import get_user_model
# from core.models import Users as LaravelUser  # adjust this if your model name is different

# User = get_user_model()
  

# class LaravelBackend:
#     def authenticate(self, request, username=None, password=None ,email=None):
#         if username is None or password is None:
#             return None

#         # 1) Try Laravel user
#         try:
#             laravel_user = LaravelUser.objects.get(email=username)
#             stored = (laravel_user.password or '').strip()

#             # Handle 'bcrypt_sha256$$...' prefix
#             # if stored.startswith('bcrypt_sha256$$'):
#             #     stored = stored.split('$$', 1)[1]  # keep only the $2b$... part

#             # Find the first $2 bcrypt string
#             idx = stored.find('$2')
#             if idx != -1:
#                 bcrypt_blob = stored[idx:].encode('utf-8')

#                 # Normalize Laravel $2y$ → $2b$ for Python
#                 bcrypt_blob = bcrypt_blob.replace(b"$2y$", b"$2b$")

#                 print(bcrypt_blob)

#                 try:
#                     if bcrypt.checkpw(password.encode('utf-8'), bcrypt_blob):
#                         # Get or create corresponding Django user
#                         user, created = User.objects.get_or_create(
#                             email=laravel_user.email,
#                             defaults={'name': getattr(laravel_user, 'name', '')}
#                         )
#                         # Optional: rehash into Django default hasher
#                         # user.set_password(password)
#                         # user.save(update_fields=['password'])
#                         return user
#                 except ValueError:
#                     # Malformed bcrypt — ignore and fall through
#                     pass
#         except LaravelUser.DoesNotExist:
#             pass

#         # 2) Fallback: regular Django user
#         try:
#             user = User.objects.get(email=username)
#             if user.check_password(password):
#                 return user
#         except User.DoesNotExist:
#             pass

#         return None

#     def get_user(self, user_id):
#         try:
#             return User.objects.get(pk=user_id)
#         except User.DoesNotExist:
#             return None