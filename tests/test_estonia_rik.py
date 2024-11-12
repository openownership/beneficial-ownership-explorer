import json
import pytest

from boexplorer.search import (fetch_all_data, fetch_person_data, process_data,
                               process_person_data)
from boexplorer.apis.estonia_rik import EstoniaRIK
from boexplorer import config

@pytest.mark.asyncio
async def test_estonia_rik():
    config.app_config = {"caching": {"cache_dir": "cache"}}
    api = EstoniaRIK()
    text = "Alexela"
    bods_data = {'entities': {}, 'persons': {}, 'sources': {}}
    _, company_data, persons_data = await fetch_all_data(api, text, bods_data)
    process_data(company_data, persons_data, api, bods_data, search=text)

    print(json.dumps(bods_data, indent=2))
    assert False

@pytest.mark.asyncio
async def test_estonia_rik_person_search():
    config.app_config = {"caching": {"cache_dir": "cache"}}
    api = EstoniaRIK()
    text = "Jüri Mõis"
    bods_data = {'persons': {}, 'sources': {}}
    _, persons_data = await fetch_person_data(api, text, bods_data)
    process_person_data(persons_data, api, bods_data, search=text)

    print(json.dumps(bods_data, indent=2))
    assert False
