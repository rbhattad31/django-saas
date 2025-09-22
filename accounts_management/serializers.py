from rest_framework import serializers
from core.models import Users,Account
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from datetime import datetime

class UserSerializer(serializers.ModelSerializer):
    role_name = serializers.SerializerMethodField()
    account_names = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    created_date = serializers.SerializerMethodField()

    class Meta:
        model = Users
        fields = ['id', 'name', 'email', 'mobile_number', 'status', 'created_date', 'role_name', 'account_names']

    def get_role_name(self, obj):
        groups = obj.groups.all()
        return groups[0].name if groups else 'N/A'

    def get_account_names(self, obj):
        return obj.account.account_name if obj.account else 'N/A'

    def get_status(self, obj):
        return 'Active' if obj.is_active else 'Inactive'

    def get_created_date(self, obj):
        return obj.created_at.strftime('%d-%m-%Y') if obj.created_at else 'N/A'
 
    
    # def get_user_status(self, obj):
    #     return 'Y' if obj.is_active else 'N'
    
class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirmpassword = serializers.CharField(write_only=True)
    role = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(), write_only=True)
    account = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all())
    created_at = serializers.DateTimeField(required=False)

    class Meta:
        model = Users
        fields = ['name', 'email', 'mobile_number', 'password', 'confirmpassword', 'role', 'account', 'timezone', 'additional_info',"created_at"]

    def validate(self, data):
        if data['password'] != data['confirmpassword']:
            raise serializers.ValidationError({"confirmpassword": "Passwords do not match."})
        return data

    def create(self, validated_data):
        role = validated_data.pop('role')
        confirmpassword = validated_data.pop('confirmpassword')
        created_at = validated_data.pop('created_at', None)
        user = Users.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            name=validated_data['name'],
            mobile_number=validated_data['mobile_number'],
            timezone=validated_data.get('timezone'),
            additional_info=validated_data.get('additional_info'),
            account=validated_data['account']
        )
        if created_at:
            user.created_at = created_at  # Manually set timestamp
            user.save()
        user.groups.add(role)
        user.save()
        return user
class UpdateUserSerializer(serializers.ModelSerializer):
    role = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(), write_only=True)
    account = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all(), allow_null=True)
    image_path = serializers.ImageField(source='image', required=False, allow_null=True)  # Map image_path to image
    remove_image = serializers.BooleanField(required=False, default=False)  # Flag for image removal

    class Meta:
        model = Users
        fields = ['name', 'email', 'mobile_number', 'role', 'account', 'timezone', 'additional_info', 'is_active','image_path', 'remove_image']

    def validate(self, data):
        email = data.get('email')
        if email and Users.objects.filter(email=email).exclude(id=self.instance.id).exists():
            raise serializers.ValidationError({"email": "Email already exists."})
        return data
    
    def validate_image_path(self, value):
        if value:
            # Validate file size (3MB = 3 * 1024 * 1024 bytes)
            if value.size > 3 * 1024 * 1024:
                raise serializers.ValidationError("Image size should be less than 3 MB.")
            # Validate file type
            valid_extensions = ['jpg', 'jpeg', 'png', 'gif']
            ext = value.name.split('.')[-1].lower()
            if ext not in valid_extensions:
                raise serializers.ValidationError("Invalid image file type. Allowed types: jpg, jpeg, png, gif.")
        return value

    def update(self, instance, validated_data):

        if validated_data.get('remove_image', False):
            if instance.image:  # Check if image exists before deleting
                instance.image.delete()  # Delete the image file from storage
                instance.image = None
        role = validated_data.pop('role', None)
        image = validated_data.pop('image', None)
        instance.name = validated_data.get('name', instance.name)
        instance.email = validated_data.get('email', instance.email)
        instance.mobile_number = validated_data.get('mobile_number', instance.mobile_number)
        instance.timezone = validated_data.get('timezone', instance.timezone)
        instance.additional_info = validated_data.get('additional_info', instance.additional_info)
        instance.account = validated_data.get('account', instance.account)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        # Handle image upload
        if image and not validated_data.get('remove_image', False):
            instance.image = image
        if role:
            instance.groups.clear()
            instance.groups.add(role)
        instance.save()
        print("DEBUG: Updated user timezone:", instance.timezone)
        print("DEBUG: Updated user image:", instance.image)
        return instance