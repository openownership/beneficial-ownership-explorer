import asyncio
import pytest
import tempfile

from boexplorer.download.caching import cache_init, write_cache, read_cache, build_cache_key

@pytest.fixture
def temporary_directory():
    return tempfile.TemporaryDirectory()

@pytest.mark.asyncio
async def test_caching(temporary_directory):
    cache = cache_init(override=temporary_directory)
    key = build_cache_key("https://api.statistics.sk/rpo/v1/search",
                          {'fullName': 'Transpetrol'},
                          {'limit': 25, 'page': 1})
    data = "foo"
    await write_cache(cache, key, data)
    await asyncio.sleep(2)
    assert read_cache(cache, key) == data

