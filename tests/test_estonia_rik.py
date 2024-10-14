import json
import pytest

from boexplorer.search import fetch_all_data, process_data
from boexplorer.apis.estonia_rik import EstoniaRIK

@pytest.mark.asyncio
async def test_estonia_rik():
    api = EstoniaRIK()
    text = "Alexela"
    bods_data = {'entities': {}, 'persons': {}, 'sources': {}}
    _, company_data, persons_data = await fetch_all_data(api, text, bods_data)
    process_data(company_data, persons_data, api, bods_data, search=text)

    print(json.dumps(bods_data, indent=2))
    assert False
