import asyncio
import json
import pycountry

from boexplorer.apis import search_companies_apis, search_persons_apis
from boexplorer.download.query import download_json
from boexplorer.query.name import (build_company_id_query, build_company_name_query,
                                   build_company_persons_query)
from boexplorer.query.person import build_person_name_query, build_person_id_query
from boexplorer.transforms.bods_0_4_0 import transform_entity, transform_person


def add_source(api, data, entity_count, person_count):
    source_id = api.scheme
    if api.scheme.split('-')[0] == "XI":
        country = "Global"
    else:
        country = pycountry.countries.get(alpha_2=api.scheme.split('-')[0]).name
    data[source_id] = {'code': api.source_description,
                               'name': api.scheme_name,
                               'country': country,
                               'url': api.search_url,
                               'entity_count': entity_count,
                               'person_count': person_count}

def match_records(entities, data):
    counter = {}
    for entity in entities:
        record_id = entity["recordId"]
        if record_id in data:
            data[entity["recordId"]].append(entity)
        else:
            data[entity["recordId"]] = [entity]
        counter[record_id] = None
    return len(counter)

def process_data(company_data, person_data, api, bods_data, search=None):
    entities = []
    persons = []
    links = []
    for item in company_data:
        #print("Company item:", item)
        if not api.filter_result(item, search=search):
            print("Transforming ...")
            entities.append(transform_entity(item, api))
        #links.extend(api.extract_links(item))
    #for link in links:
    #    json_data = download_json(url, {})
    #    if api.extract_type(json_data) == "relationship":
    for item in person_data:
        #print("Person item:", item)
        if not api.filter_result(item, search_type="company"):
            print("Transforming ...")
            persons.append(transform_person(item, api))
    entity_count = match_records(entities, bods_data['entities'])
    person_count = match_records(persons, bods_data['persons'])
    add_source(api, bods_data['sources'], entity_count, person_count)

def process_person_data(source_data, api, bods_data, search=None):
    print("Processing:", len(source_data))
    persons = []
    links = []
    for item in source_data:
        print("Person item:", item, api.filter_result(item, search_type="person"))
        if not api.filter_result(item, search_type="person"):
            print("Transforming ...")
            persons.append(transform_person(item, api))
    print(json.dumps(persons, indent=2))
    person_count = match_records(persons, bods_data['persons'])
    add_source(api, bods_data['sources'], 0, person_count)

async def fetch_all_data(api, text, bods_data, max_results=100):
    page_number = 1
    page_size = 25
    raw_data = []
    count = 0
    user_agent, cookie = api.session_cookie
    header = {}
    if user_agent: header["User-Agent"] = user_agent
    if cookie: header["Cookie"] = cookie
    while True:
        url, query_params, other_params = build_company_name_query(api,
                                                                   text,
                                                                   page_size=page_size,
                                                                   page_number=page_number)
        json_data = await download_json(url, query_params, other_params,
                                  post=api.http_post["company_search"],
                                  post_pagination=api.post_pagination,
                                  post_json=isinstance(query_params, dict),
                                  json_data=api.return_json["company_search"],
                                  header=header,
                                  auth=api.authenticator if not (isinstance(api.authenticator, dict) and
                                                             not 'Authorization' in api.authenticator)
                                                             else None)
        if not api.check_result(json_data):
            break
        data = api.extract_data(json_data)
        if data:
            print(json.dumps(data, indent=2))
            raw_data.extend(data)
            count += len(data)
            if len(data) < page_size or count >= max_results:
                break
            page_number += 1
        else:
            break
    if api.http_post["company_detail"] is not None and raw_data:
        company_data = []
        for entity in raw_data:
            url, params = build_company_id_query(api, entity)
            json_data = await download_json(url, params, {},
                                      post=api.http_post["company_detail"],
                                      header=header,
                                      auth=api.authenticator if not (isinstance(api.authenticator, dict) and
                                                             not 'Authorization' in api.authenticator)
                                                             else None)
            if api.check_result(json_data, detail=True):
                company_data.append(json_data)
                api.company_prepocessing(json_data)
    else:
        company_data = raw_data
    persons_data = []
    if (api.http_post["company_persons"] is not None or
        (api.http_post["company_persons"] is None and
         api.return_json["company_persons"])) and company_data:
        for entity in company_data:
            if (api.http_post["company_persons"] is not None and api.company_persons_url(entity) and
                not api.filter_result(entity, search_type="company_persons", search=text)):
                #print(api.identifier(entity), api.filter_result(entity, search_type="company_persons"))
                url, params = build_company_persons_query(api, entity)
                #print(url, params)
                json_data = await download_json(url, params, {},
                                  verify=False,
                                  post=api.http_post["company_persons"],
                                  post_pagination=api.post_pagination,
                                  post_json=isinstance(params, dict),
                                  json_data=api.return_json["company_persons"],
                                  header=header,
                                  auth=api.authenticator if not (isinstance(api.authenticator, dict) and
                                                             not 'Authorization' in api.authenticator)
                                                             else None)
            else:
                json_data = company_data
            print("Return type", type(json_data))
            for person in api.extract_entity_persons_items(json_data):
                persons_data.append(person)
    return api, company_data, persons_data

async def fetch_person_data(api, text, bods_data, max_results=100):
    page_number = 1
    page_size = 25
    raw_data = []
    count = 0
    user_agent, cookie = api.session_cookie
    header = {}
    if user_agent: header["User-Agent"] = user_agent
    if cookie: header["Cookie"] = cookie
    while True:
        url, query_params, other_params = build_person_name_query(api,
                                                                  text,
                                                                  page_size=page_size,
                                                                  page_number=page_number)
        json_data = await download_json(url, query_params, other_params,
                                  post=api.http_post["person_search"],
                                  post_pagination=api.post_pagination,
                                  post_json=isinstance(query_params, dict),
                                  json_data=api.return_json["person_search"],
                                  header=header,
                                  auth=api.authenticator if not (isinstance(api.authenticator, dict) and
                                                             not 'Authorization' in api.authenticator)
                                                             else None,
                                  timeout=api.http_timeout)
        print(json.dumps(json_data, indent=2))
        #if not api.check_result(json_data):
        #    break
        data = api.extract_data(json_data)
        if data:
            print(json.dumps(data, indent=2))
            raw_data.extend(data)
            count += len(data)
            if len(data) < page_size or count >= max_results:
                break
            page_number += 1
        else:
            break
    if api.http_post["person_detail"] is not None and raw_data:
        person_data = []
        for person in raw_data:
            url, params = build_person_id_query(api, person)
            json_data = await download_json(url, params, {},
                                      post=api.http_post["person_detail"],
                                      header=header,
                                      auth=api.authenticator if not (isinstance(api.authenticator, dict) and
                                                             not 'Authorization' in api.authenticator)
                                                             else None,
                                      timeout=api.http_timeout)
            print("Raw data:", json.dumps(json_data, indent=2))
            if api.check_result(json_data, detail=True):
                if isinstance(json_data, list):
                    person_data.extend(json_data)
                else:
                    person_data.append(json_data)
                api.person_prepocessing(json_data)
    else:
        person_data = raw_data
    return api, person_data

async def perform_company_search(text):
    bods_data = {'entities': {}, 'persons': {}, 'sources': {}}
    tasks = [fetch_all_data(api, text, bods_data) for api in search_companies_apis]

    # schedule the tasks and retrieve results
    results = await asyncio.gather(*tasks)

    for result in results:
        process_data(result[1], result[2], result[0], bods_data, search=text)

    return bods_data

async def perform_person_search(text):
    bods_data = {'persons': {}, 'sources': {}}

    tasks = [fetch_person_data(api, text, bods_data) for api in search_persons_apis]

    # schedule the tasks and retrieve results
    results = await asyncio.gather(*tasks)

    for result in results:
        process_person_data(result[1], result[0], bods_data, search=text)
    #for api in search_persons_apis:
    #    person_data = await fetch_person_data(api, text, bods_data)
    #    process_person_data(person_data, api, bods_data)
    return bods_data
