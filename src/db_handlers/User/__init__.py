# import json

# user_data = User(json.loads(request.form["user"]))
# user_data.created = datetime.datetime.now().isoformat()
# user_data.matches = []

# creator, err = User.from_token(request.cookies.get("token"))
# isSelfCreated = creator is None or Perms.CREATE_USERS not in creator.perms_list

# if isSelfCreated or not user_data.perms:
#     user_data.set_perms(UNCONDITIONAL_PERM_LIST)

from src.errors import handle_err, UserNotFoundError
from src.perms import decode_perms

global config
global jwt

def attr_or_none(obj, attr):
    try:
        return obj[attr]
    except (AttributeError, KeyError):
        return None

def remove_none(dict):
    return { k: v for k, v in dict.items() if v is not None }

class User():

    """Database handler representing a user, changes have to be followed by .save().

    Leave one blank line.  The rest of this docstring should contain an
    overall description of the module or program.  Optionally, it may also
    contain a brief description of exported classes and functions and/or usage
    examples.

      Typical usage example:

      user = User(db, user_data).create()

      user = User.from_query(db, { "name": "Linus Bolls" })

      user = User.from_email(db, "linus.bolls@code.berlin")

      user = User.from_token(db, request.cookies.get("token"))

      user.add_perms([ Perms.CREATE_USERS ])
      user.save()
    """

    # ===== Basics ===== #

    def __init__(self, db, user_data):

        self.db = db
        self.created = attr_or_none(user_data, "created")
        self.email = attr_or_none(user_data, "email")
        self.name = attr_or_none(user_data, "name")
        self.img = attr_or_none(user_data, "img")
        self.matches = attr_or_none(user_data, "matches")
        self.perms_int = attr_or_none(user_data, "perms_int")
        self.perms_list = decode_perms(self.perms_int)

    def from_query(db, db_query):
  
        try:
            user_data = db.users.find_one(db_query)

            if user_data is None:
                raise UserNotFoundError

            return ( User(db, user_data), None )

        except Exception as e:
            return ( None, handle_err(e) )

    def from_email(db, email):

        return User.from_query(db, { "email": email })

    def from_token(db, token):
  
        token_data, err = jwt.decode_token(token)

        if err:
            return ( None, handle_err(err) )

        return ( User.from_email(db, token_data["email"]), None )
    
    def __save_or_create(self, is_create):
  
        user = remove_none({         
            "created": self.created,
            "email": self.email,
            "name": self.name,
            "img": self.img,
            "matches": self.matches,
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

    from src.db_handlers.User.auth import set_perms, add_perms, make_token, make_magic_link