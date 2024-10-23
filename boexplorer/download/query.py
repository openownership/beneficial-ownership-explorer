import asyncio
import json
import logging

import httpx
from parsel import Selector

from boexplorer.download.utils import get_random_user_agent
from boexplorer.download.caching import write_cache, read_cache, build_cache_key

logging.basicConfig(
    format="%(levelname)s [%(asctime)s] %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.DEBUG
)

def parse_html(html_text):
    selector = Selector(text=html_text)
    return selector.xpath('//body')

async def save_cache(cache, key, data):
    if not cache is None:
        if isinstance(data, str):
            await write_cache(cache, key, data)
        else:
            await write_cache(cache, key, json.dumps(data))
    return data

async def download_json(api_url, query_params, other_params, json_data=True, auth=None,
                  post=False, post_json=True, post_pagination=False, header=None, random_ua=True,
                  verify=True, return_header=False, timeout=15, cache=None):
    if json_data:
        headers = {"Accept": "application/json",
                   "Content-Type": "application/json"}
    else:
        headers = {"Accept": "text/html,application/xhtml+xml,application/xml"}
    if header:
        for h in header:
            headers[h] = header[h]
    if isinstance(auth, dict):
        for a in auth:
            headers[a] = auth[a]
        auth = None
    if random_ua:
        headers["User-Agent"] = get_random_user_agent()
    print("Headers:", headers, "URL:", api_url, "Post:", post,
          "Params:", query_params, other_params, "Cache:", cache)
    if not cache is None:
        key = build_cache_key(api_url, query_params, other_params)
        cached_data = read_cache(cache, key)
        if cached_data:
            print("Retreiving cached data ...")
            return cached_data
    else:
        key = None
    client = httpx.AsyncClient(verify=verify)
    response = None
    try:
        if post:
            if post_json:
                if post_pagination:
                    if len(query_params) == 1 and isinstance(query_params[next(iter(query_params))], dict):
                        key = next(iter(query_params))
                        query_params[key] = query_params[key] | other_params
                        params = query_params
                    else:
                        if query_params is None or other_params is None:
                            await asyncio.sleep(5)
                            print("Alert:", api_url, query_params, other_params)
                        params = query_params | other_params
                    print("Post params:", params)
                    response = await client.post(api_url,
                               params={},
                               json=params,
                               auth=auth,
                               headers=headers,
                               timeout=timeout)
                else:
                    response = await client.post(api_url,
                               params=other_params,
                               json=query_params,
                               auth=auth,
                               headers=headers,
                               timeout=timeout)
            else:
                response = await client.post(api_url,
                               params=other_params,
                               data=query_params,
                               auth=auth,
                               headers=headers,
                               timeout=timeout)
        else:
            if query_params is None or other_params is None:
                await asyncio.sleep(5)
                print("Alert:", api_url, query_params, other_params)
            params = query_params | other_params
            response = await client.get(api_url, params=params, auth=auth, headers=headers,
                              timeout=timeout)
    except httpx.HTTPError as exception:
        print(f"HTTP Exception for {exception.request.url} - {exception}")
    finally:
        await client.aclose()
    #print(response)
    print(cache, key)
    if response and response.status_code == 200:
        if json_data:
            try:
                return await save_cache(cache, key, response.json())
            except json.decoder.JSONDecodeError:
                return []
        else:
            if return_header:
                return response.header
            else:
                return await save_cache(cache, key, response.text)
    else:
        return []
