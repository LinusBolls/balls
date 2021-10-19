from .atomics_schema import created_schema, game_schema
from .team_schema import team_schema

match_schema = {
    "bsonType": "object",
    "required": [ "created", "game", "teams" ],
    "properties": {
        "id": {
            "bsonType": "string",
            "description": "md5 hash of the amount of existing matches"
        },
        "created": created_schema,
        "game": game_schema,
        "teams": {
            "bsonType": [ "array" ],
            "items": team_schema,
            "description": "The teams that participated in the match"
        }
    }
}