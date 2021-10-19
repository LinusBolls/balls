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

from src.perms import encode_perms, Perms, UNCONDITIONAL_PERM_LIST, MAIL_CONFIRMED_PERM_LIST

linus, linus_err = User(db, {
    "created": datetime.now(),
    "email": "linus.bolls@code.berlin",
    "name": "Linus Bolls",
    "elo": {},
    "perms_int": encode_perms(list(Perms)),
}).create()

tom, tom_err = User(db, {
    "created": datetime.now(),
    "email": "tom-perry.lustig@code.berlin",
    "name": "Semi aquatic, egg-laying mammal of action",
    "elo": {},
    "perms_int": encode_perms(UNCONDITIONAL_PERM_LIST),
}).create()

# try:
#     user, create_err = User.from_email(db, "tom-perry.lustig@code.berlin")

#     _, save_err = user.add_perms(MAIL_CONFIRMED_PERM_LIST).save()

#     if create_err:
#         raise create_err
#     if save_err:
#         raise save_err

# except Exception as create_err:
#     print(create_err)

test_match, _ = Match(db, { 
    "created": datetime.now(),
    "game": "chess", 
    "teams": [ 
        { "created": datetime.now(), "members": [
            { "email": "linus.bolls@code.berlin", "result": 2 },
            { "email": "tom-perry.lustig@code.berlin", "result": 5 }
          ] }
    ] 
}).create()

chess_grandmasters = get_best_users_in_game(db, "chess")
print(chess_grandmasters)
print(db.matches.find_one())

"""
TODO: improve match.id
TODO: change match_player.result if match is changed
TODO: add BE_RANKED perm
TODO: add game elo_functions
"""