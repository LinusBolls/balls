from datetime import datetime

from src.errors import handle_err, UserNotFoundError
from src.perms import decode_perms
import src.jwt_token as jwt

def set_if_exists(key, src, target):
    if key in src:
        target[key] = src[key]

def attr(obj, key, fallback = None):
    return obj[key] if key in obj else fallback

def remove_none(dict):
    return { k: v for k, v in dict.items() if v is not None }

class User():

    """Database handler representing a user, changes have to be followed by .save().

    Leave one blank line.  The rest of this docstring should contain an
    overall description of the module or program.  Optionally, it may also
    contain a brief description of exported classes and functions and/or usage
    examples.

      Typical usage example:

      user, err = User(db, user_data).create()

      user, err = User.from_query(db, { "name": "Linus Bolls" })

      user, err = User.from_email(db, "linus.bolls@code.berlin")

      user, err = User.from_token(db, request.cookies.get("token"))

      user.add_perms([ Perms.CREATE_USERS ])
      user.save()
    """

    # ===== Basics ===== #

    def update_info(self, user_data):
        # set_if_exists("name", self, user_data)
        # set_if_exists("img", self, user_data)

        if "name" in user_data:
            self.name = user_data["name"]
        if "img" in user_data:
            self.img = user_data["img"]
        return self

    def __init__(self, db, user_data=None):

        self.db = db
        self.created = attr(user_data, "created")
        self.email = attr(user_data, "email")
        self.name = attr(user_data, "name")
        self.img = attr(user_data, "img")
        self.matches = attr(user_data, "matches")
        self.elo = attr(user_data, "elo")
        self.perms_int = attr(user_data, "perms_int")
        self.perms_list = decode_perms(self.perms_int)

    def from_query(db, db_query):
  
        try:
            user_data = db.users.find_one(db_query)

            if user_data is None:
                raise UserNotFoundError

            return ( User(db, user_data), None )

        except Exception as e:
            return ( None, handle_err(e) )

    def from_email(db, email=None):

        return User.from_query(db, { "email": email })

    def from_token(db, token=None):
  
        token_data, err = jwt.validate_token(token)

        if err:
            return ( None, handle_err(err) )

        return User.from_email(db, token_data["email"])
    
    def __save_or_create(self, is_create):
  
        user = remove_none({         
            "created": self.created,
            "email": self.email,
            "name": self.name,
            "img": self.img,
            "matches": self.matches,
            "elo": self.elo,
            "perms_int": self.perms_int,
        })

        try:
            if is_create:
                result = self.db.users.insert_one(user)
                return ( result.inserted_id is not None, None )
            else:
                result = self.db.users.replace_one({ "email": self.email }, user)
                return ( result.modified_count > 0, None )
        except Exception as e:
            return ( None, handle_err(e) )

    def create(self):
        return self.__save_or_create(True)
      
    def save(self):
        return self.__save_or_create(False)
    
    def delete(self):
        return ( self.db.users.delete_one({ "email": self.email }).deleted_count == 1, None)
    
    def get_data(self, exclude=[], include=[]):

        if len(include) > 0:
            data = {}
            for key in include:
                is_date = isinstance(self[key], datetime)
                data[key] = str(self[key]) if is_date else self[key]

        else:
            data = {
                "created": str(self.created),
                "email": self.email,
                "name": self.name,
                "img": self.img,
                "matches": self.matches,
                "elo": self.elo,
                "perms_int": self.perms_int
            }

        for field in exclude:
            del data[field]

        return data

    from src.db_handlers.User.auth import set_perms, add_perms, make_token, make_magic_link