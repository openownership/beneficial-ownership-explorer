import httpx
import json

def authenticate(auth_url, client_id, client_secret):
    print("Authenticating:", {"username": client_id, "password": client_secret})
    r = httpx.post(auth_url, json={"username": client_id, "password": client_secret}, timeout=15)
    json_data = r.json()
    #print(json.dumps(json_data))
    return json_data['token']

def authenticator(username="", password="", auth_type="basic", auth_url=None):
    if auth_type == "basic":
        return httpx.BasicAuth(username=username, password=password)
    elif auth_type == "bearer":
        token = authenticate(auth_url, username, password)
        return {'Authorization': f'Bearer {token}'}
    return None
