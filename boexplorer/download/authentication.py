import httpx


def authenticator(username="", password="", auth_type="basic"):
    if auth_type == "basic":
        return httpx.BasicAuth(username=username, password=password)
    return None
