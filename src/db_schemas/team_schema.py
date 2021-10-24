from .atomics_schema import created_schema
from .match_player_schema import match_player_schema

team_schema = {
    "bsonType": "object",
    "required": [ "created", "members" ],
    "properties": {
        "created": created_schema,
        "members": {
            "bsonType": [ "array" ],
            "items": match_player_schema,
            "description": "The matches the user has played"
        }
    }
}