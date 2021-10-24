from datetime import datetime, timedelta

from flask import make_response, request
from flask_restful import Resource, reqparse

from src.globals import db, api, config
from src.errors import handle_err
from src.perms import Perms, encode_perms, UNCONDITIONAL_PERM_LIST
from src.db_handlers.User import User

def make_cookie(payload, expiry_days, is_httponly=True):

    cookie = f"{ payload }; Path=/"

    if expiry_days is not None:
        # if the expires field is empty on a cookie, it will last for the length of the browser session
        expiry_date = datetime.utcnow() + timedelta(days=expiry_days)
        expiry_date_str = expiry_date.strftime("%a, %d %b %Y %H:%M:%S GMT")
        cookie += f"; expires={ expiry_date_str }"

    # HttpOnly cookies cannot be accessed by js using document.cookie, they are only sent with requests
    # this makes them more resistant to xss attacks
    if is_httponly:
        cookie += "; HttpOnly"
    return cookie

class PostUser(Resource):
    def parse(self):
        parser = reqparse.RequestParser()
        parser.add_argument("email", type=str, required=True)
        parser.add_argument("name", type=str, required=True)
        parser.add_argument("img", type=str, required=True)

        return parser.parse_args()

    def post(self):
        try:            
            creator, err = User.from_token(db, request.cookies.get("token"))

            is_self_created = creator is None or Perms.CREATE_USERS not in creator.perms_list

            user_data = self.parse()
            user_data["created"] = datetime.now()
            user_data["matches"] = []
            user_data["elo"] = {}

            if is_self_created or user_data["perms_int"] is None:
                user_data["perms_int"] = encode_perms(UNCONDITIONAL_PERM_LIST)

            user = User(db, user_data)
            is_successful, err = user.create()

            if err:
                return { "ok": 0, "err": err.msg }, err.status
    
            res = make_response({ "ok": 1, "data": user.get_data() }, 201)
            res.headers["Set-Cookie"] = make_cookie(f"token={ user.make_token() }", 7, True)
            # 7 should be cookie expiry date in days, doesnt work tho but whatever
            return res

        except Exception as err:
            handle_err(err)
            return { "ok": 0, "err": err.msg }, err.status

api.add_resource(PostUser, config["server"]["apiPath"] + "user/")