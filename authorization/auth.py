from django.conf import settings

from rest_framework.authentication import BaseAuthentication
from rest_framework.permissions import BasePermission

from authorization.utils import get_user_by_token
from authorization.validators import validate_token, validate_authorization_header
from authorization.models import User


def get_token(request):
    authorization_header = request.headers[settings.AUTH_NAME]
    validate_authorization_header(authorization_header)
    token = authorization_header.split()[1]
    validate_token(token)
    return token


class CurrentUser:
    def __init__(self, db_user: User, roles) -> None:
        self.db_user = db_user
        self.roles = roles
        self.validate()

    def validate(self):
        # compare roles from token and from db
        ...


class BaseAuthAuthentication(BaseAuthentication):

    def authenticate(self, request):
        if settings.AUTH_NAME not in request.headers:
            return None, None
        token = get_token(request)
        identifier, roles = get_user_by_token(token)

        if not User.objects.filter(identifier=identifier).exists():
            return None, None

        db_user = User.objects.get(identifier=identifier)
        current_user = CurrentUser(
            db_user=db_user,
            roles=roles
        )
        return current_user, None


class IsAuthenticated(BasePermission):
    def has_permission(self, request, view):  # noqa:W0613
        return bool(request.user)