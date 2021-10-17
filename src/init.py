from pymongo import MongoClient

from src.schemas.user_schema import user_schema
from src.schemas.match_schema import match_schema
from read_config import read_config
import send_mail

defaultConfig = {
  "server": {
    "hostname": "localhost",
    "port": 8080,
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

user_collection = db.create_collection("users", validator = { "$jsonSchema": user_schema })
user_collection = db.create_collection("matches", validator = { "$jsonSchema": match_schema })

db.users.create_index("email", unique = True)

secret = config["jwt"]["privateKey"]
send_mail.mailgunConfig = config["mailgun"]