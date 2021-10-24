from flask import request
from flask_restful import Resource

from src.globals import db, api, config
from src.db_handlers.User import User
from src.perms import Perms
from src.errors import handle_err, MissingPermissionError

class PutUser(Resource):

    def put(self, userId):

        try:
            user, err = User.from_token(db, request.cookies.get("token"))
      
            is_authorized = user is not None and (user.email == userId or Perms.MANAGE_USERS in user.perms_list)

            if not is_authorized:
                raise MissingPermissionError

            print(request.json)
            
            is_successful, err = user.update_info(request.json).save()

            if err:
                return { "ok": 0, "err": err.msg }, err.status
            return { "ok": 1, "data": user.get_data() }, 200

        except Exception as err:
            handle_err(err)
            return { "ok": 0, "err": err.msg }, err.status

api.add_resource(PutUser, config["server"]["apiPath"] + "user/<string:userId>")