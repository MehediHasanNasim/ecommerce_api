from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Profile
from .serializers import UserSerializer, GoogleSocialLoginSerializer
from django.contrib.auth import get_user_model
from dj_rest_auth.views import LoginView


User = get_user_model()

class ProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        user = self.request.user
        Profile.objects.get_or_create(user=user)  
        return user
    


class GoogleLoginView(LoginView):
    serializer_class = GoogleSocialLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        self.login(request, user)
        return Response(self.get_response_data(user))