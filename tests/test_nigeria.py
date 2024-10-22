import json
import pytest

from boexplorer.search import (fetch_all_data, fetch_person_data, process_data,
                               process_person_data)
from boexplorer.apis.nigeria_cac import NigerianCAC

@pytest.mark.asyncio
async def test_nigeria_cac_company_search():
    api = NigerianCAC()
    text = "Dangote Cement"
    bods_data = {'entities': {}, 'persons': {}, 'sources': {}}
    _, company_data, persons_data = await fetch_all_data(api, text, bods_data)
    process_data(company_data, persons_data, api, bods_data, search=text)

    print(json.dumps(bods_data, indent=2))
    assert False

@pytest.mark.asyncio
async def test_nigeria_cac_person_search():
    api = NigerianCAC()
    text = "Aliko Dangote"
    bods_data = {'persons': {}, 'sources': {}}
    _, persons_data = await fetch_person_data(api, text, bods_data)
    process_person_data(persons_data, api, bods_data, search=text)

    print(json.dumps(bods_data, indent=2))
    assert False

@pytest.mark.asyncio
async def test_nigeria_cac_person_search_2():
    api = NigerianCAC()
    text = "Charlotte Obidairo"
    bods_data = {'persons': {}, 'sources': {}}
    _, persons_data = await fetch_person_data(api, text, bods_data)
    process_person_data(persons_data, api, bods_data, search=text)

    print(json.dumps(bods_data, indent=2))
    assert False
