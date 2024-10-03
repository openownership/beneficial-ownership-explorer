import json
import pycountry

from boexplorer.apis import search_companies_apis, search_persons_apis
from boexplorer.download.query import download_json
from boexplorer.query.name import build_company_id_query, build_company_name_query
from boexplorer.query.person import build_person_name_query, build_person_id_query
from boexplorer.transforms.bods_0_4_0 import transform_entity, transform_person

def add_source_data(api, data, data_type, data_count):
    source_id = api.scheme
    if api.scheme.split('-')[0] == "XI":
        country = "Global"
    else:
        country = pycountry.countries.get(alpha_2=api.scheme.split('-')[0]).name
    if source_id in data:
        if data_type == 'entities':
            data[source_id]['entity_count'] += data_count
        elif data_type == 'persons':
            data[source_id]['person_count'] += data_count
    else:
        if data_type == 'entities':
            data[source_id] = {'code': api.source_description,
                               'name': api.scheme_name,
                               'country': country,
                               'entity_count': data_count,
                               'person_count': 0}
        elif data_type == 'persons':
            data[source_id] = {'code': api.source_description,
                               'name': api.scheme_name,
                               'country': country,
                               'entity_count': 0,
                               'person_count': data_count}

def match_records(entities, data):
    for entity in entities:
        record_id = entity["recordId"]
        if record_id in data:
            data[entity["recordId"]].append(entity)
        else:
            data[entity["recordId"]] = [entity]
    return data

def process_data(source_data, api, bods_data):
    entities = []
    links = []
    for item in source_data:
        if not api.filter_result(item):
            entities.append(transform_entity(item, api))
        #links.extend(api.extract_links(item))
    #for link in links:
    #    json_data = download_json(url, {})
    #    if api.extract_type(json_data) == "relationship":
    match_records(entities, bods_data['entities'])
    add_source_data(api, bods_data['sources'], 'entities', len(entities))

def process_person_data(source_data, api, bods_data):
    print("Processing:", len(source_data))
    persons = []
    links = []
    for item in source_data:
        print(item)
        if not api.filter_result(item):
            print("Transforming ...")
            persons.append(transform_person(item, api))
    print(json.dumps(persons, indent=2))
    match_records(persons, bods_data['persons'])
    add_source_data(api, bods_data['sources'], 'persons', len(persons))

def fetch_all_data(api, text, bods_data, max_results=100):
    page_number = 1
    page_size = 25
    raw_data = []
    count = 0
    while True:
        url, query_params, other_params = build_company_name_query(api,
                                                                   text,
                                                                   page_size=page_size,
                                                                   page_number=page_number)
        json_data = download_json(url, query_params, other_params,
                                  post=api.http_post["company_search"],
                                  post_pagination=api.post_pagination,
                                  post_json=isinstance(query_params, dict),
                                  json_data=api.return_json["company_search"],
                                  auth=api.authenticator if not (isinstance(api.authenticator, dict) and
                                                             not 'Authorization' in api.authenticator)
                                                             else None)
        print(json.dumps(json_data, indent=2))
        if not api.check_result(json_data):
            break
        data = api.extract_data(json_data)
        if data:
            print(json.dumps(data, indent=2))
            #bods_data = process_data(data, api)
            #print(json.dumps(bods_data, indent=2))
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
            json_data = download_json(url, params, {},
                                      post=api.http_post["company_detail"],
                                      auth=api.authenticator if not (isinstance(api.authenticator, dict) and
                                                             not 'Authorization' in api.authenticator)
                                                             else None)
            print(json.dumps(json_data, indent=2))
            if api.check_result(json_data, detail=True):
                #break
            #print(json.dumps(json_data, indent=2))
                company_data.append(json_data)
                api.company_prepocessing(json_data)
    else:
        company_data = raw_data
    process_data(company_data, api, bods_data)

def fetch_person_data(api, text, bods_data, max_results=100):
    page_number = 1
    page_size = 25
    raw_data = []
    count = 0
    while True:
        url, query_params, other_params = build_person_name_query(api,
                                                                  text,
                                                                  page_size=page_size,
                                                                  page_number=page_number)
        json_data = download_json(url, query_params, other_params,
                                  post=api.http_post["person_search"],
                                  post_pagination=api.post_pagination,
                                  post_json=isinstance(query_params, dict),
                                  json_data=api.return_json["person_search"],
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
            json_data = download_json(url, params, {},
                                      post=api.http_post["person_detail"],
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
    process_person_data(person_data, api, bods_data)

def perform_company_search(text):
    bods_data = {'entities': {}, 'sources': {}}
    for api in search_companies_apis:
        fetch_all_data(api, text, bods_data)
    return bods_data

def perform_person_search(text):
    bods_data = {'persons': {}, 'sources': {}}
    for api in search_persons_apis:
        fetch_person_data(api, text, bods_data)
    return bods_data
