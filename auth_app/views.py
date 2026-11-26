from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from .serializers import RegisterSerializer


class RegisterView(APIView):
    """Register a new user."""

    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        """Validate registration data and create a user."""
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {'detail': 'User created successfully!'},
            status=status.HTTP_201_CREATED
        )
