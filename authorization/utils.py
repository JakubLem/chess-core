import json
from jose import jws, jwt
from django.conf import settings
from authorization.exceptions import UnauthenticatedException


def get_user_by_token(token):
    try:
        claims = jws.get_unverified_claims(
            token
        )
    except jwt.JWSError as e:
        raise UnauthenticatedException(f"Invalid token, detail: {e}")

    decoded_claims = json.loads(claims.decode())

    if settings.SUB_KEY not in decoded_claims:
        raise UnauthenticatedException("Missing sub_key in claims")

    identifier = decoded_claims[settings.SUB_KEY]
    roles = None
    try:
        roles = decoded_claims[settings.REALM_ACCESS_CLAIM][settings.ROLES_FIELD]
    except:  # noqa:E722
        pass

    return identifier, roles