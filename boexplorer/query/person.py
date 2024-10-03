def build_person_name_query(api, text, page_size=100, page_number=1):
    query_params = api.query_person_name_params(api.to_local_characters(text))
    if isinstance(query_params, dict):
        if api.query_person_name_extra: query_params = query_params | api.query_person_name_extra
        other_params = {}
        if api.page_size_par[0]:
            if api.page_size_par[1]:
                other_params[api.page_size_par[0]] = [min(api.page_size_max, page_size)]
            else:
                other_params[api.page_size_par[0]] = min(api.page_size_max, page_size)
        if api.page_number_par[0]:
            if api.page_number_par[1] == 0:
                page_number = page_number - 1
            other_params[api.page_number_par[0]] = page_number
    else:
        other_params = {}
    return api.person_search_url, query_params, other_params

def build_person_id_query(api, person):
    params = api.query_person_detail_params(person)
    if api.query_person_detail_extra: params = params | api.query_person_detail_extra
    return api.person_detail_url(person), params
