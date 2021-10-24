from flask import Flask
from flask_restful import Api

import src.globals as globals

globals.init()

app = Flask(__name__)
api = Api(app)

globals.api = api

# ===== Registering Endpoints ===== #

import endpoints.user.post # cookie[CREATE_USERS]? user_data
import endpoints.user.get # <user_id>
# import endpoints.user.put # cookie[MANAGE_USERS or email=email], user_data
# import endpoints.user.delete # cookie[MANAGE_USERS or email=email], user_id

import endpoints.match.post # cookie[CREATE_MATCHES], match_data
import endpoints.match.get # <match_id>
# import endpoints.match.put # cookie[MANAGE_MATCHES], match_data
# import endpoints.match.delete # cookie[MANAGE_MATCHES], match_id

# import endpoints.magic.get # <secret_key>
# import endpoints.magic.post # email

import endpoints.ranking.get # <gameId> results: int

if __name__ == "__main__":
    config = globals.config
    app.run(host = config["server"]["hostname"], port = config["server"]["port"], debug = config["isTesting"])

# flask_restful gold: https://blog.miguelgrinberg.com/post/designing-a-restful-api-using-flask-restful
# sql_alchemy gold: https://www.robinwieruch.de/postgres-sql-macos-setup
# jwt: https://auth0.com/blog/how-to-handle-jwt-in-python/

# TODO: implement BE_RANKED perm
# TODO: implement game rules
# TODO: implement teams for events to fix the setting created in teams hack
# TODO: make .get_data(include) possible
# TODO: make cookie expiry date possible
