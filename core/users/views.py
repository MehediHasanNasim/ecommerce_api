from rest_framework import generics, permissions
from .models import Profile
from .serializers import UserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class ProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        user = self.request.user
        Profile.objects.get_or_create(user=user)  
        return user