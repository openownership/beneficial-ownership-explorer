import json
import pytest

from boexplorer.search import fetch_all_data, fetch_person_data, process_data
from boexplorer.apis.bulgaria_cr import BulgarianCR

@pytest.mark.asyncio
async def test_bulgaria_cr():
    api = BulgarianCR()
    text = "Aurubis"
    bods_data = {'entities': {}, 'persons': {}, 'sources': {}}
    _, company_data, persons_data = await fetch_all_data(api, text, bods_data)
    process_data(company_data, persons_data, api, bods_data, search=text)

    print(json.dumps(bods_data, indent=2))

    assert bods_data[0]["statementId"] == "8fbe1039-3341-59ec-d07a-0590d38513a3"
    assert bods_data[0]["recordId"] == "BG-EIK-832046871"
    assert bods_data[1]["statementId"] == "d4e5823a-4c51-78f2-b184-17cc378fb81d"
    assert bods_data[1]["recordId"] == "BG-EIK-121472418"

    assert False

#@pytest.mark.asyncio
#async def test_bulgaria_cr_person_search():
#    api = BulgarianCR()
#    text = "Harings"
#    bods_data = {'persons': {}, 'sources': {}}
#    await fetch_person_data(api, text, bods_data)
#    print(json.dumps(bods_data, indent=2))
#    assert False


