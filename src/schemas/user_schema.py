from .atomics_schema import created_schema, email_schema

user_schema = {
    "bsonType": "object",
    "additionalProperties": True,
    "required": [ "email", "created", "perms_int" ],
    "properties": {
        "created": created_schema,
        "perms_int": {
            "bsonType": "int",
            "description": "A power of two that represents an array of permissions"
        },
        "email": email_schema,
        "name": {
            "bsonType": "string",
            "description": "Nickname, optional"
        },
        "img": {
            "bsonType": "string",
            "description": "Profile picture url, optional"
        },
        "matches": {
            "bsonType": [ "array" ],
            "items": {
                "bsonType": "string",
                "description": "Match id"
            },
            "description": "The matches the user has played"
        }
    }
}