from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.exceptions import TokenError

from .serializers import LoginSerializer, RegisterSerializer
from .utils import (
    generate_tokens,
    get_login_data,
    set_auth_cookies,
    get_refresh_response,
    get_unauthorized_response,
    refresh_access_token,
)


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


class LoginView(APIView):
    """Authenticate a user and issue JWT cookies."""

    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        """Validate credentials and return JWT cookies."""
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {'detail': 'Invalid username or password.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        user = serializer.validated_data['user']
        tokens = generate_tokens(user)
        response = Response(get_login_data(user), status=status.HTTP_200_OK)
        set_auth_cookies(response, tokens)
        return response


class TokenRefreshView(APIView):
    """Refresh the access token using the refresh cookie."""

    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        """Refresh the access token from the request cookie."""
        refresh_token = request.COOKIES.get('refresh_token')
        if not refresh_token:
            return get_unauthorized_response('Refresh token is missing.')
        try:
            access_token = refresh_access_token(refresh_token)
        except TokenError:
            return get_unauthorized_response('Invalid refresh token.')
        return get_refresh_response(access_token)
