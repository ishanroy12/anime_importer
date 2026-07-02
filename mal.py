import requests
import os
import json
import secrets
import webbrowser
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("MAL_CLIENT_ID")
TOKEN_FILE = "mal_token.json"

def generate_pkce():
    code_verifier = secrets.token_urlsafe(100)[:128]
    return code_verifier

def get_token():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as f:
            return json.load(f)["access_token"]
    
    code_verifier = generate_pkce()
    
    auth_url = (
        f"https://myanimelist.net/v1/oauth2/authorize"
        f"?response_type=code"
        f"&client_id={CLIENT_ID}"
        f"&code_challenge={code_verifier}"
        f"&code_challenge_method=plain"
    )
    
    print("Opening browser for MAL authorization...")
    webbrowser.open(auth_url)
    
    auth_code = input("Paste the authorization code from the URL here: ")
    
    response = requests.post(
        "https://myanimelist.net/v1/oauth2/token",
        data={
            "client_id": CLIENT_ID,
            "grant_type": "authorization_code",
            "code": auth_code,
            "code_verifier": code_verifier,
        }
    )
    
    token_data = response.json()
    print(token_data)
    
    with open(TOKEN_FILE, "w") as f:
        json.dump(token_data, f)
    
    return token_data["access_token"]

def search_anime(title, access_token):
    response = requests.get(
        "https://api.myanimelist.net/v2/anime",
        headers={"Authorization": f"Bearer {access_token}"},
        params={"q": title, "limit": 1}
    )
    data = response.json()
    if not data["data"]:
        return None
    return data["data"][0]["node"]["id"]

def add_to_ptw(title):
    access_token = get_token()
    
    anime_id = search_anime(title, access_token)
    if not anime_id:
        print(f"Could not find {title} on MAL")
        return False
    
    response = requests.patch(
        f"https://api.myanimelist.net/v2/anime/{anime_id}/my_list_status",
        headers={"Authorization": f"Bearer {access_token}"},
        data={"status": "plan_to_watch"}
    )
    
    if response.status_code == 200:
        print(f"Added {title} to PTW")
        return True
    else:
        print(f"Failed to add {title}")
        return False