from datetime import datetime
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from src.init import config, db
from src.db_handlers.User import User
from src.db_handlers.Match import Match
import src.send_mail as mail
import src.jwt_token as jwt
from src.rankings import get_best_users_in_game

mail.mailgunConfig = config["mailgun"]
jwt.secret = config["jwt"]["privateKey"]

User.jwt = jwt
User.config = config

def now():
    return datetime.now()

from src.perms import encode_perms, Perms, UNCONDITIONAL_PERM_LIST, MAIL_CONFIRMED_PERM_LIST

linus = User(db, {
    "created": now(),
    "email": "linus.bolls@code.berlin",
    "name": "Linus Bolls",
    "elo": {
        "chess": 5
    },
    "perms_int": encode_perms(list(Perms)),
})
tom = User(db, {
    "created": now(),
    "email": "tom-perry.lustig@code.berlin",
    "name": "Semi aquatic, egg-laying mammal of action",
    "elo": {
        "chess": 7
    },
    "perms_int": encode_perms(UNCONDITIONAL_PERM_LIST),
})
_, linus_err = linus.create()
_, tom_err = tom.create()

tom_obj, err = User.from_email(db, "tom-perry.lustig@code.berlin")

tom_obj.add_perms(MAIL_CONFIRMED_PERM_LIST).save()

test_match = Match(db, { 
    "created": now(), 
    "game": "chess", 
    "teams": [ 
        { "created": "now", "members": [
            { "email": "linus.bolls@code.berlin", "elo": 5, "result": 5 },
            { "email": "tom-perry.lustig@code.berlin", "elo": 5, "result": 5 }
          ] }
    ] 
})
test_match.create()
print(get_best_users_in_game(db, "chess", 99))