from flask_restful import Resource

from src.globals import db, api, config
from src.db_handlers.Match import Match

class GetMatch(Resource):

    def get(self, matchId):

        match, err = Match.from_query(db, { "id": matchId })

        if err:
            return { "ok": 0, "err": err.msg }, err.status
        return { "ok": 1, "data": match.get_data() }, 200

api.add_resource(GetMatch, config["server"]["apiPath"] + "match/<string:matchId>")