

from rest_framework import serializers
from core.models import Users
from django.utils.html import format_html


class  UserSerializer(serializers.ModelSerializer):
  class Meta :
    model = Users
    field = "__all__"










class UsersfilterSerilizer(serializers.Serializer):
    draw = serializers.IntegerField(required=False)
    start = serializers.IntegerField(required=False)
    length = serializers.IntegerField(required=False)
    search = serializers.DictField(required=False)