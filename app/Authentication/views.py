from rest_framework.permissions import IsAuthenticated

from .models import CustomUser
from rest_framework import generics
from .serializers import UserSerializer, UserLocationSerializer


class UserRegister(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


class UserProfileUpdateView(generics.UpdateAPIView):
    serializer_class = UserLocationSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
