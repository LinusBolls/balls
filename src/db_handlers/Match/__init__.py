from src.errors import handle_err, UserNotFoundError
from src.perms import decode_perms

global config
global jwt

def attr(obj, key, fallback = None):
    return obj[key] if key in obj else fallback

def remove_none(dict):
    return { k: v for k, v in dict.items() if v is not None }

class Match():

    def __init__(self, db, match_data):

        self.db = db
        self.created = attr(match_data, "created")
        self.game = attr(match_data, "game")
        self.teams = attr(match_data, "teams")

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

        db_members = self.db.users.find(find_users_query)

        members_all_exist = db_members.count() == len(self.team_members)

        if not members_all_exist:
            return ( None, UserNotFoundError )

        matchId = "moin"

        for team in self.teams:
            for member in team["members"]:
                ding = self.db.users.find_one_and_update({ "email": member["email"] }, { "$push": { "matches": matchId }, "$inc": { f"elo.{self.game}": member["result"] } })
                previous_elo = attr(ding["elo"], self.game, 0)
                member["elo"] = previous_elo

        success, err = self.__save_or_create(True)

        if err:
            return ( success, err )

        return ( True, None )
      
    def save(self):
        return self.__save_or_create(False)