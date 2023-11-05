from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response


def get_user_location(request):
    User = get_user_model()
    user = User.objects.get(pk=request.user.pk)
    if not user.location:
        return Response({'message': 'Your location is not set.'}, status=status.HTTP_404_NOT_FOUND)
    return user.location
