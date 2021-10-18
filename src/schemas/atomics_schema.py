game_schema = {
    "enum": [ "fooooosball", "chess" ],
    "description": "TODO: Make enum"
}
created_schema = {
    "bsonType": "date",
    "description": "Creation time"
}
email_schema = {
    "bsonType": "string",
    "description": "Serves as UUID"
}
elo_schema = {
    "bsonType": "int",
    "description": "Elo of the player at the time of playing"
}
result_schema = {
    "bsonType": "int",
    "description": "Result of the game for the player"
}