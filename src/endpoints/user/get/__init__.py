from flask import request
from flask_restful import Resource

from src.globals import db, api, config
from src.db_handlers.User import User
from src.perms import Perms, assert_has_permissions

class GetUser(Resource):

    def get(self, userId):

        assert_has_permissions(User.from_token(db, request.cookies.get("token"))[0], [ Perms.VIEW_USERS ])

        user, err = User.from_email(db, userId)

        if err:
            return { "ok": 0, "err": err.msg }, err.status
        return { "ok": 1, "data": user.get_data() }, 200

api.add_resource(GetUser, config["server"]["apiPath"] + "user/<string:userId>")