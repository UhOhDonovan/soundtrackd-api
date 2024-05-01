# test the spotify api
from dotenv import main
from requests import post, get
import os
import base64
import json

main.load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")


def get_token():
    authorization_str = (client_id + ":" + client_secret).encode("utf-8")
    authorization_str = str(base64.b64encode(authorization_str), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + authorization_str,
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {"grant_type": "client_credentials"}

    response = post(url, headers=headers, data=data)
    token = json.loads(response.content)["access_token"]
    return token


def get_auth_header(token):
    return {"Authorization": "Bearer " + token}


def search_album(token, name):
    url = "https://api.spotify.com/v1/search"
    headers = {"Authorization": "Bearer " + token}
    query = f"?q={name}&type=album&limit=10"
    query_url = url + query
    response = get(query_url, headers=headers)
    result = json.loads(response.content)["albums"]["items"]
    print(result)
    return result
def get_album(albumid, token):
    url = f"https://api.spotify.com/v1/albums/{albumid}"
    headers = {"Authorization": "Bearer " + token}
    response = get(url, headers=headers)
    return json.loads(response.content)

var = "hello"
print("\33[4m" + f"test {var}" + "\033[0m")
search = input("Enter an album to search: ")
search_results = search_album(get_token(), search)
for i in range(10):
    print(f"-----Result {i + 1}:-----")
    print(f"Title: {search_results[i]["name"]} ({search_results[i]["release_date"][:4]})")
    print("Artist:", search_results[i]["artists"][0]["name"])
    print("Link:", search_results[i]["external_urls"]["spotify"])

print(json.dumps(get_album(search_results[0]["id"], get_token()), indent=2))
