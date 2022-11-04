from rest_framework.exceptions import APIException


class AuthAPIException(APIException):
    def __init__(self, detail=None, code=None):
        super().__init__(detail=detail, code=code)
        self.code = code


class BadRequest(AuthAPIException):
    status_code = 400


class ConflictRequest(AuthAPIException):
    status_code = 409


class UnauthenticatedException(AuthAPIException):
    status_code = 401
