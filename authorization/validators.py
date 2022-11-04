import json
from datetime import datetime
from jose import jws, jwt
from django.conf import settings
from authorization.exceptions import UnauthenticatedException, BadRequest


def check_token_exp(exp):
    return exp >= int(datetime.now().timestamp())


def validate_token(token):
    try:
        claims = jws.get_unverified_claims(
           token
        )
    except jwt.JWSError as e:
        raise BadRequest(detail=e)

    decoded_claims = json.loads(claims.decode())
    exp = decoded_claims.get(settings.EXP_KEY)
    if not check_token_exp(exp):
        raise UnauthenticatedException(f"Invalid token {settings.EXP_KEY}")


def validate_authorization_header(header):
    splited = header.split()

    if len(splited) != 2:
        raise UnauthenticatedException("Invalid header")

    if splited[0] != settings.AUTH_PREFIX:
        raise UnauthenticatedException("Invalid header")


def validate_password(password):
    special_chars =['$', '!', '@', '#', '%', '&']
    validated = True
    msg = ' '

    if len(password) < 8:
        msg = 'Password length must be at least 8'
        validated = False
    elif len(password) > 18:
        msg = 'Password length must not be greater than 18'
        validated = False
    elif not any(char.isdigit() for char in password):
        msg = 'Password should have at least one number'
        validated = False
    elif not any(char.isupper() for char in password):
        msg = 'Password should have at least one uppercase letter'
        validated = False
    elif not any(char.islower() for char in password):
        msg = 'Password should have at least one lowercase letter'
        validated = False
    elif not any(char in special_chars for char in password):
        msg = 'Password should have at least one special character'
        validated = False
    return { 'is_valid': validated, 'message': msg }
