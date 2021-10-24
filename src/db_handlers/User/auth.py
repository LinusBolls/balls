from secrets import token_urlsafe

from src.globals import config
from src.errors import handle_err, UserNotFoundError
from src.perms import encode_perms
import src.send_mail as mail
import src.jwt_token as jwt

def make_token(self):
    """
      Returns str
    """
    return jwt.make_token({ "email": self.email, "perms": self.perms_int })

def make_magic_link(self):
    """
      Returns ( bool, err )
    """

    try:
        token = token_urlsafe(8)
        link = f"https://randomuser.me/magic/{self.email}/{token}"

        setTokenQuery = { "$set": { "token": hash(token) }}

        if not config["isTestMode"]:
            mail.send_mail([ self.email ], "Your Magic Login Link", link)

        result = self.db.users.update_one({ "email": self.email }, setTokenQuery)

        if (result.modified_count == 0):
            raise UserNotFoundError

        return ( token if config["isTestMode"] else True, None )

    except Exception as err:
        return ( None, handle_err(err) )

def set_perms(self, new_perms_list):
    """
      Returns User
    """
    self.perms_list = new_perms_list
    self.perms_int = encode_perms(new_perms_list)

    return self

def add_perms(self, perms_list):
    """
      Returns User
    """
    perms_list = list(map(lambda x : None if x in self.perms_list else x, perms_list))
    return self.set_perms(self.perms_list + perms_list)