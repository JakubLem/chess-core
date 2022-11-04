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