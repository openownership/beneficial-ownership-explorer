import json
import pytest

from boexplorer.search import fetch_all_data, process_data
from boexplorer.apis.gleif import GLEIF
from boexplorer.data.data import load_data
from boexplorer import config

@pytest.mark.asyncio
async def test_gleif():
    config.app_config = {"caching": {"cache_dir": "cache"}}
    scheme_data = load_data()
    api = GLEIF(scheme_data)
    text = "Aurubis"
    bods_data = {'entities': {}, 'persons': {}, 'sources': {}}
    _, company_data, persons_data = await fetch_all_data(api, text, bods_data)
    process_data(company_data, persons_data, api, bods_data, search=text)

    print(json.dumps(bods_data, indent=2))

    assert bods_data[0]["statementId"] == "0871c4da-1c83-a457-6002-bdb1c128d3f1"
    assert bods_data[0]["recordId"] == "DE-CR-HRB 1775"
    assert bods_data[1]["statementId"] == "76870c27-48f0-2f3e-c26b-971b466c12ef"
    assert bods_data[1]["recordId"] == "BG-EIK-832046871"
    assert bods_data[2]["statementId"] == "a3feab91-5d15-99c2-4096-3da38c70b44b"
    assert bods_data[2]["recordId"] == "BE-BCE_KBO-0873.533.993"
    assert bods_data[3]["statementId"] == "8950cbf6-b60f-c4a0-c854-250a9ba1bc50"
    assert bods_data[3]["recordId"] == "ES-RMC-BI-2699B-8"
    assert bods_data[4]["statementId"] == "fe21aa87-1a0e-4008-8282-02d072dbffc6"
    assert bods_data[4]["recordId"] == "CH-FDJP-CHE-109.600.069"
    assert bods_data[5]["statementId"] == "1b81ad83-ce94-511a-d5ae-0d3d7229dd84"
    assert bods_data[5]["recordId"] == "SE-BLV-556030-2480"
    assert bods_data[6]["statementId"] == "5d154195-0761-5b63-e41a-352c6283bdf2"
    assert bods_data[6]["recordId"] == "FI-PRO-2413477-5"
    assert bods_data[7]["statementId"] == "dc4c7ab3-57be-9d62-3b98-4fff0fbf9fd5"
    assert bods_data[7]["recordId"] == "GB-COH-05169749"
    assert bods_data[8]["statementId"] == "1dcc2fd5-0366-5668-cd45-252989e7f22d"
    assert bods_data[8]["recordId"] == "NL-KVK-52930610"
    assert bods_data[9]["statementId"] == "da824d00-d452-d9eb-6613-41fda68970c8"
    assert bods_data[9]["recordId"] == "SK-ORSR-36737062"
    assert bods_data[10]["statementId"] == "359e4750-d591-403f-e88f-69648b71ffa2"
    assert bods_data[10]["recordId"] == "DE-CR-HRA 5603"
    assert bods_data[11]["statementId"] == "1aebd904-ab4c-e7a7-676a-1fcf11abdfb2"
    assert bods_data[11]["recordId"] == "BE-BCE_KBO-0403075580"
