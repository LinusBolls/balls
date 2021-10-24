import jwt

from src.errors import handle_err, JwtDecryptError
from src.globals import config

secret = config["jwt"]["privateKey"]

def validate_token(token):
    try:
        if not isinstance(token, str):
            raise JwtDecryptError
        return ( jwt.decode(token, secret, algorithms=["HS256"]), None )

    except Exception as err:
        return ( None, handle_err(err) )

def make_token(payload):
    return jwt.encode(payload, secret, "HS256")

# cmd + space spotlight!