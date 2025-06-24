from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from .models import CustomUser, Profile

class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        model = CustomUser
        fields = ('email', 'password', 'first_name', 'last_name')

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)  # From User model
    bio = serializers.CharField(source='profile.bio', read_only=True)
    birth_date = serializers.DateField(source='profile.birth_date', read_only=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'bio', 'birth_date')