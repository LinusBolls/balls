from flask import request
from flask_restful import Resource

from src.globals import db, api, config
from src.rankings import get_best_users_in_game

class GetRanking(Resource):

    def get(self, gameId):

        results = request.args["results"]
        results_int_or_none = int(results) if results.isdigit() else None

        data = get_best_users_in_game(db, gameId, results_int_or_none)
    
        return { "ok": 1, "data": data }, 200

api.add_resource(GetRanking, config["server"]["apiPath"] + "ranking/<string:gameId>")