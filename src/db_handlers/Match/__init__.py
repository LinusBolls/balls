from src.errors import handle_err, UserNotFoundError
from src.perms import decode_perms

global config
global jwt

def attr_or_none(obj, attr):
    try:
        return obj[attr]
    except (AttributeError, KeyError):
        return None

def remove_none(dict):
    return { k: v for k, v in dict.items() if v is not None }

class Match():

    def __init__(self, db, match_data):

        self.db = db
        self.created = attr_or_none(match_data, "created")
        self.game = attr_or_none(match_data, "game")
        self.teams = attr_or_none(match_data, "teams")

        team_members = []

        for i in list(map(lambda team: team["members"], self.teams)):
            for y in i:
                team_members.append(y["email"])

        self.team_members = team_members
    
    def __save_or_create(self, is_create):
  
        match = remove_none({         
            "created": self.created,
            "game": self.game,
            "teams": self.teams,
        })

        try:
            if is_create:
                result = self.db.matches.insert_one(match)
                return ( result.inserted_id is not None, None )
            else:
                result = self.db.matches.replace_one({ "email": self.email }, match)
                return ( result.modified_count > 0, None )

        except Exception as e:
            return ( None, handle_err(e) )

    def create(self):

        find_users_query = { "email": { "$in": self.team_members }}

        # db_members = self.db.users.find(find_users_query)

        # members_all_exist = db_members.count() == len(self.team_members)

        # if not members_all_exist:
        #     return ( None, UserNotFoundError )

        success, err = self.__save_or_create(True)

        if err:
            return ( success, err )

        matchId = "moin"

        result = self.db.users.update_many(find_users_query, { "$push": { "matches": matchId } })
        return ( result.modified_count == len(self.team_members), None )
      
    def save(self):
        return self.__save_or_create(False)