import json
import logging

import httpx
from parsel import Selector

from boexplorer.download.utils import get_random_user_agent

logging.basicConfig(
    format="%(levelname)s [%(asctime)s] %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.DEBUG
)

def parse_html(html_text):
    selector = Selector(text=html_text)
    return selector.xpath('//body')

def authenticate(auth_url, client_id, client_secret):
    r = httpx.post(auth_url, json={"username": client_id, "password": client_secret})
    json_data = r.json()
    print(json.dumps(json_data))
    return json_data['token']

def download_json(api_url, query_params, other_params, json_data=True, auth=None, token=None,
                  post=False, post_json=True, post_pagination=False, header=None, random_ua=True,
                  verify=True, timeout=15):
    if json_data:
        headers = {"Accept": "application/json",
                   "Content-Type": "application/json"}
    else:
        headers = {"Accept": "text/html,application/xhtml+xml,application/xml"}
    if header:
        for h in header:
            headers[h] = header[h]
    if token:
        headers['Authorization'] = f'Bearer {token}'
    if random_ua:
        headers["User-Agent"] = get_random_user_agent()
    print("Headers:", headers, "URL:", api_url, "Post:", post, "Params:", query_params, other_params)
    client = httpx.Client(verify=verify)
    if post:
        if post_json:
            if post_pagination:
                if len(query_params) == 1 and isinstance(query_params[next(iter(query_params))], dict):
                    key = next(iter(query_params))
                    query_params[key] = query_params[key] | other_params
                    params = query_params
                else:
                    params = query_params | other_params
                print("Post params:", params)
                response = client.post(api_url,
                               params={},
                               json=params,
                               auth=auth,
                               headers=headers,
                               timeout=timeout)
            else:
                response = client.post(api_url,
                               params=other_params,
                               json=query_params,
                               auth=auth,
                               headers=headers,
                               timeout=timeout)
        else:
                response = client.post(api_url,
                               params=other_params,
                               data=query_params,
                               auth=auth,
                               headers=headers,
                               timeout=timeout)
    else:
        params = query_params | other_params
        response = client.get(api_url, params=params, auth=auth, headers=headers,
                              timeout=timeout)
    client.close()
    print(response)
    if response.status_code == 200:
        if json_data:
            try:
                return response.json()
            except json.decoder.JSONDecodeError:
                return []
        else:
            return response.text
    else:
        return []
