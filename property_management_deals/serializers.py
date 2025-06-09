from rest_framework import serializers
from .models import Property
from django.contrib.auth.models import User

# class PropertySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Property
#         fields = '__all__'
# serializers.py
# from rest_framework import serializers
# from .models import Property
# from django.contrib.auth.models import User

# class PropertySerializer(serializers.ModelSerializer):
#     agent_name = serializers.SlugRelatedField(
#         slug_field='username',
#         queryset=User.objects.all()
#     )

#     class Meta:
#         model = Property
#         fields = '__all__'
class PropertySerializer(serializers.ModelSerializer):
    agent_name = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )
    owner_source = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )
    agent1 = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )
    agent2 = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
        allow_null=True,
        required=False
    )
    agent3 = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
        allow_null=True,
        required=False
    )

    class Meta:
        model = Property
        fields = '__all__'

