from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


def generate_tokens(user):
    """Generate access and refresh tokens for a user."""
    refresh = RefreshToken.for_user(user)

    return {
        'access': str(refresh.access_token),
        'refresh': str(refresh),
    }


def set_auth_cookie(response, name, token, lifetime):
    """Set a secure authentication cookie."""
    response.set_cookie(
        key=name,
        value=token,
        max_age=int(lifetime.total_seconds()),
        httponly=True,
        secure=settings.AUTH_COOKIE_SECURE,
        samesite=settings.AUTH_COOKIE_SAMESITE,
    )


def set_access_cookie(response, access_token):
    """Attach the access token cookie to the response."""
    set_auth_cookie(
        response, 'access_token', access_token,
        settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
    )


def set_auth_cookies(response, tokens):
    """Attach access and refresh cookies to the response."""
    set_auth_cookie(
        response, 'access_token', tokens['access'],
        settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
    )
    set_auth_cookie(
        response, 'refresh_token', tokens['refresh'],
        settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME']
    )


def get_login_data(user):
    """Build the successful login response data."""
    return {
        'detail': 'Login successfully!',
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
        }
    }


def get_refresh_response(access_token):
    """Build the successful token refresh response."""
    response = Response(
        {'detail': 'Token refreshed'},
        status=status.HTTP_200_OK
    )
    set_access_cookie(response, access_token)
    return response


def get_unauthorized_response(message):
    """Build an unauthorized response with an error message."""
    return Response(
        {'detail': message},
        status=status.HTTP_401_UNAUTHORIZED
    )


def refresh_access_token(refresh_token):
    """Generate a new access token using the provided refresh token."""
    refresh = RefreshToken(refresh_token)
    validate_refresh_user(refresh)
    return str(refresh.access_token)


def validate_refresh_user(refresh):
    """Ensure the token belongs to an active user."""
    user_id = refresh.get('user_id')
    if not user_id:
        raise TokenError("Token has no user ID.")
    if not User.objects.filter(id=user_id, is_active=True).exists():
        raise TokenError("User is not active or does not exist.")
