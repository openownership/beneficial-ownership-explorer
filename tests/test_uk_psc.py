import json
import pytest

from boexplorer.search import fetch_all_data, process_data
from boexplorer.apis.uk_psc import UKPSC

@pytest.mark.asyncio
async def test_uk_psc():
    api = UKPSC()
    text = "AstraZeneca"
    text = "Metro Bank"
    bods_data = {'entities': {}, 'persons': {}, 'sources': {}}
    _, company_data, persons_data = await fetch_all_data(api, text, bods_data)
    process_data(company_data, persons_data, api, bods_data, search=text)
    print(json.dumps(company_data, indent=2))
    print(json.dumps(persons_data, indent=2))
    print(json.dumps(bods_data, indent=2))
    assert False
