from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken


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
