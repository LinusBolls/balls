from .atomics_schema import email_schema, elo_schema, result_schema

match_player_schema = {
    "bsonType": "object",
    "required": [ "email", "elo", "result" ],
    "properties": {
        "email": email_schema,
        "elo": elo_schema,
        "result": result_schema
    }
}