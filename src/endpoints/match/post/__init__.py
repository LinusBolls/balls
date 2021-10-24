from datetime import datetime

from flask import make_response, request
from flask_restful import Resource, reqparse

from src.globals import db, api, config
from src.errors import handle_err, MissingPermissionError
from src.perms import Perms
from src.db_handlers.User import User
from src.db_handlers.Match import Match

class PostMatch(Resource):
    def parse(self):
        parser = reqparse.RequestParser()
        parser.add_argument("game", type=str, required=True)
        parser.add_argument("teams", type=list[object], required=True)
        # RequestParser apparently is not able to parse nested json such as teams,
        # so we access teams seperately by request.json["teams"] below

        return parser.parse_args()

    def post(self):
        try:
            creator, err = User.from_token(db, request.cookies.get("token"))

            if creator is None or Perms.CREATE_MATCHES not in creator.perms_list:
                raise MissingPermissionError

            match_data = self.parse()
            match_data["created"] = datetime.now()
            match_data["teams"] = request.json["teams"]

            for team in match_data["teams"]:
                team["created"] = datetime.now()

            match = Match(db, match_data)
            is_successful, err = match.create()

            if err:
                return { "ok": 0, "err": err.msg }, err.status
            # make_response necessary to stringify datetime.datetime for some reason
            return make_response({ "ok": 1, "data": match.get_data() }, 201)

        except Exception as err:
            handle_err(err)
            return { "ok": 0, "err": err.msg }, err.status

api.add_resource(PostMatch, config["server"]["apiPath"] + "match/")