import asyncio
import hashlib
import json
from diskcache import Cache

def build_cache_key(url, params, other_params):
    params = json.dumps(params, sort_keys=True)
    other_params = json.dumps(other_params, sort_keys=True)
    data = f"{url}{params}{other_params}"
    return hashlib.sha256(data.encode("utf-8")).hexdigest()

def cache_init(cache_dir):
    return Cache(cache_dir)

async def write_cache(cache, key, data):
    print("Writing to key:", key, "Data length:", len(data))
    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(None, cache.set, key, data)
    return result

def read_cache(cache, key):
    if key in cache:
        try:
            return json.loads(cache[key])
        except:
            return cache[key]
    else:
        return None
