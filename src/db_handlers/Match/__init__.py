from datetime import datetime
import hashlib

from src.errors import handle_err, MatchNotFoundError, UserNotFoundError

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
    
    def from_query(db, db_query):
  
        try:
            match_data = db.matches.find_one(db_query)

            if match_data is None:
                raise MatchNotFoundError

            return ( Match(db, match_data), None )

        except Exception as e:
            return ( None, handle_err(e) )
    
    def __save_or_create(self, is_create):
  
        match = remove_none({         
            "created": self.created,
            "game": self.game,
            "teams": self.teams,
            "id": self.id,
        })

        try:
            if is_create:
                result = self.db.matches.insert_one(match)
                self.id = result.inserted_id
                return ( result.inserted_id is not None, None )
            else:
                result = self.db.matches.replace_one({ "email": self.email }, match)
                return ( result.modified_count > 0, None )

        except Exception as e:
            return ( None, handle_err(e) )

    def create(self):

        find_users_query = { "email": { "$in": self.team_members }}
        print(self.team_members)

        members_all_exist = self.db.users.find(find_users_query).count() == len(self.team_members)

        if not members_all_exist:
            return ( None, UserNotFoundError )

        self.id = hashlib.md5(str(self.db.matches.count()).encode("utf-8")).hexdigest()

        for team in self.teams:
            for member in team["members"]:
                ding = self.db.users.find_one_and_update({ "email": member["email"] }, { "$push": { "matches": self.id }, "$inc": { f"elo.{self.game}": member["result"] } })
                previous_elo = attr(ding["elo"], self.game, 0)
                member["elo"] = previous_elo

        success, err = self.__save_or_create(True)
        if err:
            return ( success, err )

        return ( True, None )
      
    def save(self):
        return self.__save_or_create(False)

    def get_data(self, exclude=[], include=[]):

        if len(include) > 0:
            data = {}
            for key in include:
                is_date = isinstance(self[key], datetime)
                data[key] = str(self[key]) if is_date else self[key]

        else:
            data = {
                "created": str(self.created),
                "game": self.game,
                "teams": self.teams,
            }

        for field in exclude:
            del data[field]

        return data