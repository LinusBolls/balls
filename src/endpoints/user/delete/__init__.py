from flask import request
from flask_restful import Resource

from src.globals import db, api, config
from src.db_handlers.User import User
from src.perms import Perms, has_permissions
from src.errors import handle_err, MissingPermissionError

class DeleteUser(Resource):

    def delete(self, userId):

        try:
            user, err = User.from_token(db, request.cookies.get("token"))

            is_authorized = (user is not None and user.email == userId) or has_permissions(user, [ Perms.MANAGE_USERS ])

            if not is_authorized:
                raise MissingPermissionError

            is_successful, err = user.delete()

            if not is_successful:
                raise Exception

            if err:
                return { "ok": 0, "err": err.msg }, err.status
            return { "ok": 1, "data": user.get_data() }, 200

        except Exception as err:
            print(err)
            handle_err(err)
            print(err.msg)
            return { "ok": 0, "err": err.msg }, err.status


api.add_resource(DeleteUser, config["server"]["apiPath"] + "user/<string:userId>")