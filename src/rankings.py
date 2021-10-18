import pymongo

def attr(obj, key, fallback = None):
    return obj[key] if key in obj else fallback

def get_best_users_in_game(db, game, max):

    users = db.users.aggregate([
        {
            "$match": {
                f"elo.{game}": { "$exists": True }
            }
        },
        {
            "$sort": {
                f"elo.{game}": pymongo.DESCENDING,
            }
        },
        {
          "$limit": max
        }
    ])

    user_map = lambda user: {
        "email": user["email"], 
        "name": attr(user, "name", ""),
        "img": attr(user, "img", ""),
        "elo": user["elo"][game],
    }
    return list(map(user_map, users))