from flask import request
from flask_restful import Resource

from src.globals import db, api, config
from src.db_handlers.Match import Match
from src.perms import Perms, assert_has_permissions
from src.db_handlers.User import User

class GetMatch(Resource):

    def get(self, matchId):

        assert_has_permissions(User.from_token(db, request.cookies.get("token"))[0], [ Perms.VIEW_MATCHES ])

        match, err = Match.from_query(db, { "id": matchId })

        if err:
            return { "ok": 0, "err": err.msg }, err.status
        return { "ok": 1, "data": match.get_data() }, 200

api.add_resource(GetMatch, config["server"]["apiPath"] + "match/<string:matchId>")