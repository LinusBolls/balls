from datetime import datetime
import requests
import json

res = requests.post("http://localhost:8080/api/v1/user/", { "email": "linus.bolls@code.berlin", "name": "Linus Bolls", "img": "" })
assert res.status_code == 201

res = requests.post("http://localhost:8080/api/v1/user/", { "email": "tom-perry.lustig@code.berlin", "name": "Perry :)", "img": "" })
assert res.status_code == 201

cookie = res.headers["Set-Cookie"]

res = requests.get("http://localhost:8080/api/v1/user/linus.bolls@code.berlin")
assert res.json()["data"]["name"] == "Linus Bolls"

res = requests.get("http://localhost:8080/api/v1/user/nonexistent.user@code.berlin")
assert res.status_code == 404


res = requests.get("http://localhost:8080/api/v1/match/nonexistent_matchid")
assert res.status_code == 404

res = requests.post("http://localhost:8080/api/v1/match/", json={ "game": "chess", "teams": [ 
        { "created": str(datetime.now()), "members": [ { "email": "linus.bolls@code.berlin", "result": 2 } ] },
        { "created": str(datetime.now()), "members": [ { "email": "tom-perry.lustig@code.berlin", "result": 5 } ] }
    ]  }, headers={ "Cookie": cookie })
assert res.status_code == 201