from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from .models import CustomUser, Profile
from dj_rest_auth.serializers import LoginSerializer
from allauth.socialaccount.models import SocialAccount


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


class CustomLoginSerializer(LoginSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, attrs):
        attrs = super().validate(attrs)
        return attrs

class GoogleSocialLoginSerializer(serializers.Serializer):
    access_token = serializers.CharField(required=True)
    
    def validate(self, attrs):
        access_token = attrs.get('access_token')
        try:
            # Verify token with Google
            from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
            from allauth.socialaccount.providers.oauth2.client import OAuth2Client
            adapter = GoogleOAuth2Adapter()
            token = adapter.parse_token({'access_token': access_token})
            login = adapter.complete_login(request=None, app=None, token=token)
            user = login.account.user
            attrs['user'] = user
            return attrs
        except Exception as e:
            raise serializers.ValidationError(str(e))