config = None
api = None
db = None

def init():
    global config
    global db

    from pymongo import MongoClient

    from src.db_schemas.user_schema import user_schema
    from src.db_schemas.match_schema import match_schema
    from src.read_config import read_config

    defaultConfig = {
      "server": {
        "hostname": "localhost",
        "port": 8080,
        "apiPath": "/api/v1/"
      },
      "mailgun": {
        "hostname": "",
        "privateKey": "",
      },
      "mongoDb": {
        "url": "mongodb://localhost:27017/",
        "collection": "code",
      },
      "jwt": {
          "privateKey": "replaceThisWithRandomlyGeneratedStringInProd",
      },
      "isTesting": True,
    }
    config = read_config(defaultConfig, "../config.json")

    client = MongoClient(config["mongoDb"]["url"])
    db = client[config["mongoDb"]["collection"]]

    db.users.drop()
    db.matches.drop()

    db.create_collection("users", validator = { "$jsonSchema": user_schema })
    db.create_collection("matches", validator = { "$jsonSchema": match_schema })

    db.users.create_index("email", unique = True)