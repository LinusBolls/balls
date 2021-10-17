import datetime
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from src.init import config, db
from src.db_handlers.User import User
from src.db_handlers.Match import Match
import src.send_mail as mail
import src.jwt_token as jwt

mail.mailgunConfig = config["mailgun"]
jwt.secret = config["jwt"]["privateKey"]

User.jwt = jwt
User.config = config

from src.perms import encode_perms, Perms, UNCONDITIONAL_PERM_LIST, MAIL_CONFIRMED_PERM_LIST

linus = User(db, {
    "created": datetime.datetime.now().isoformat(),
    "email": "linus.bolls@code.berlin",
    "name": "Linus Bolls",
    "perms_int": encode_perms(list(Perms)),
})
tom = User(db, {
    "created": datetime.datetime.now().isoformat(),
    "email": "tom-perry.lustig@code.berlin",
    "name": "Semi aquatic, egg-laying mammal of action",
    "perms_int": encode_perms(UNCONDITIONAL_PERM_LIST),
})
linus.create()
tom.create()

tom_obj, err = User.from_email(db, "tom-perry.lustig@code.berlin")

if not err:
    tom_obj.add_perms(MAIL_CONFIRMED_PERM_LIST).save()
print(tom_obj.perms_list)

test_match = Match(db, { 
    "created": datetime.datetime.now().isoformat(), 
    "game": "chess", 
    "teams": [ 
        { "created": "now", "members": [
            { "email": "linus.bolls@code.berlin", "elo": 5, "result": 5 },
            { "email": "tom-perry.lustig@code.berlin", "elo": 5, "result": 5 }
          ] }
    ] 
})
success, err = test_match.create()