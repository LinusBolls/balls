import jwt

from src.errors import handle_err

global secret

class JwtDecryptError(Exception):
    status = 403
    msg = "Failed to decrypt jwt token"

def validate_token(token):

    try:
        if not isinstance(token, str):
            raise JwtDecryptError()
        return ( jwt.decode(token, secret, algorithms = ["HS256"]), None )

    except Exception as err:
        return ( None, handle_err(err) )