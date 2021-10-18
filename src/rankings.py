import pymongo

def attr(obj, key, fallback = None):
    return obj[key] if key in obj else fallback

def get_best_users_in_game(db, game, max_results = None):

    # TODO: add BE_RANKED perm

    query = [
        {
            "$match": {
                f"elo.{game}": { "$exists": True }
            }
        },
        {
            "$sort": {
                f"elo.{game}": pymongo.DESCENDING,
            }
        }
    ]
    if max_results is not None:
        query.append({ "$limit": max_results })

    users = db.users.aggregate(query)

    user_map = lambda user: {
        "email": user["email"], 
        "name": attr(user, "name", ""),
        "img": attr(user, "img", ""),
        "elo": user["elo"][game],
    }
    return list(map(user_map, users))