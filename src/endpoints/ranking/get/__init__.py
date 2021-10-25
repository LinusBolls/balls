from flask import request
from flask_restful import Resource

from src.globals import db, api, config
from src.rankings import get_best_users_in_game
from src.perms import Perms, assert_has_permissions
from src.db_handlers.User import User

class GetRanking(Resource):

    def get(self, gameId):

        assert_has_permissions(User.from_token(db, request.cookies.get("token"))[0], [ Perms.VIEW_RANKINGS ])

        results = request.args["results"]
        results_int_or_none = int(results) if results.isdigit() else None

        data = get_best_users_in_game(db, gameId, results_int_or_none)
    
        return { "ok": 1, "data": data }, 200

api.add_resource(GetRanking, config["server"]["apiPath"] + "ranking/<string:gameId>")