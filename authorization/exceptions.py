from rest_framework.exceptions import APIException


class AuthFailed(APIException):
    status_code = 401
