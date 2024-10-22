from typing import Optional, Tuple, Union

from boexplorer.apis.protocol import API
from boexplorer.data.data import lookup_scheme


class GLEIF(API):
    """Handle accessing GLEIF api"""
    def __init__(self, scheme_data=None):
        self.scheme_data=scheme_data

    @property
    def authenticator(self) -> str:
        """API authenticator"""
        return None

    @property
    def base_url(self) -> str:
        """API base url"""
        return "https://api.gleif.org/api/v1"

    @property
    def http_timeout(self) -> int:
        """API http method"""
        return 15

    @property
    def http_post(self) -> dict:
        """API http post"""
        return {"company_search": False,
                "company_detail": None,
                "company_persons": None,
                "person_search": None,
                "person_detail": None}

    @property
    def return_json(self) -> dict:
        """API returns json"""
        return {"company_search": True,
                "company_detail": None,
                "company_persons": None,
                "person_search": None,
                "person_detail": None}

    @property
    def post_pagination(self) -> bool:
        """API post pagination"""
        return False

    @property
    def session_cookie(self):
        return None, None

    @property
    def company_search_url(self) -> str:
        """API company search url"""
        return f"{self.base_url}/lei-records"

    def company_detail_url(self, company_data: dict) -> str:
        """API company detail url"""
        return None

    @property
    def person_search_url(self) -> str:
        """API person search url"""
        return None

    def person_detail_url(self, company_data) -> str:
        """API person detail url"""
        return None

    def to_local_characters(self, text):
        """Transliterate into local characters"""
        return text

    def from_local_characters(self, text):
        """Transliterate from local characters"""
        return text

    @property
    def page_size_par(self) -> Tuple[str, bool]:
        """Page size parameter"""
        return "page[size]", False

    @property
    def page_number_par(self) -> Tuple[str, int]:
        """Page number parameter"""
        return "page[number]", 1

    @property
    def page_size_max(self) -> int:
        """Maximum page size"""
        return 100

    def query_company_name_params(self, text: str) -> dict:
        """Querying company name parameter"""
        return {"filter[entity.names]": text}

    @property
    def query_company_name_extra(self) -> str:
        """Querying company name extra parameters"""
        return {}

    def query_company_detail_params(self, company_data: dict) -> dict:
        """Querying company detail parameters"""
        return {}

    @property
    def query_company_detail_extra(self) -> str:
        """Querying company details extra parameters"""
        return None

    def query_person_name_params(self, text) -> dict:
        """Querying person name parameter"""
        return None

    @property
    def query_person_name_extra(self) -> str:
        """Querying person name extra parameters"""
        return None

    def query_person_detail_params(self, company_data) -> dict:
        """Querying company detail parameters"""
        return None

    @property
    def query_person_detail_extra(self) -> str:
        """Querying company details extra parameters"""
        return None

    def check_result(self, json_data: Union[dict, list]) -> bool:
        """Check successful return value"""
        if isinstance(json_data, dict) and "data" in json_data:
            return True
        else:
            #if 'code' in json_data:
            #    print(f"Error: {json_data['code']} {json_data['message']}")
            return False

    def filter_result(self, data: dict, search_type=None, search=None, detail=False) -> bool:
        """Filter out item if meets condition"""
        return False

    def extract_data(self, json_data: dict) -> dict:
        """Extract main data body from json data"""
        if "data" in json_data:
            return json_data['data']
        else:
            return []

    def extract_type(self, json_data: dict) -> Optional[str]:
        """Extract item type (entity, relationship or exception)"""
        if json_data["data"]["type"] == "lei-records":
            return "entity"
        elif json_data["data"]["type"] == "relationship-records":
            return "relationship"
        elif json_data["data"]["type"] == "reporting-exceptions":
            return "exception"
        return None

    def extract_entity_item(self, data: dict) -> dict:
        """Extract entity item data"""
        return data['attributes']['entity']

    def extract_relationship_item(self, data: dict) -> dict:
        """Extract relationship item data"""
        return data['attributes']['relationship']

    def identifier(self, data: dict) -> str:
        """Get entity identifier"""
        return data["attributes"]["lei"]

    def entity_name(self, item: dict) -> str:
        """Get entity name"""
        return item['legalName']['name']

    def jurisdiction(self, item: dict) -> str:
        """Get jurisdiction"""
        return item['jurisdiction']

    @property
    def scheme(self) -> str:
        """Get scheme"""
        return 'XI-LEI'

    @property
    def search_url(self) -> str:
        """URL for manual search"""
        return 'https://search.gleif.org/#/search/'

    @property
    def scheme_name(self) -> str:
        """Get scheme name"""
        return 'Global Legal Entity Identifier Index'

    def _get_scheme(self, scheme_id):
        match = [scheme for scheme in self.scheme_data if scheme[0] == scheme_id]
        if match:
            country = match[0][2]
            return lookup_scheme(country, "company")
        return None, None

    def additional_identifiers(self, item: dict) -> list:
        """Get list of additional identifiers"""
        #print(item)
        if "registeredAs" in item:
            if item["registeredAt"]["id"] != "RA999999":
                scheme_code, scheme_name = self._get_scheme(item["registeredAt"]["id"])
                return [{'id': item["registeredAs"],
                         'scheme': scheme_code,
                         'schemeName': scheme_name}]
            else:
                return []
        else:
            return []

    def record_id(self, item: dict) -> str:
        """Get recordID"""
        additional = self.additional_identifiers(item['attributes']['entity'])
        #print(additional)
        if additional and additional[0]['scheme'] and additional[0]['id']:
            return f"{additional[0]['scheme']}-{additional[0]['id']}"
        else:
            return f"XI-LEI-{item['attributes']['lei']}"

    def registered_address(self, item: dict) -> dict:
        """Get registered address"""
        return item['legalAddress']

    def business_address(self, item: dict) -> dict:
        """Get registered address"""
        return item['headquartersAddress']

    def source_type(self, data: dict) -> str:
        """Get source type"""
        return (['officialRegister'] if not data["attributes"]['registration']["corroborationLevel"] ==
                 'FULLY_CORROBORATED' else ['officialRegister', 'verified'])

    @property
    def source_description(self) -> str:
        """Get source description"""
        return 'GLEIF'

    def address_string(self, address: dict) -> str:
        """Get address string"""
        lines = address['addressLines'] + [address['city']]
        return ", ".join(lines)

    def address_country(self, address: dict) -> str:
        """Get address country"""
        return address['country']

    def address_postcode(self, address: dict) -> Optional[str]:
        """Get address postcode"""
        if 'PostalCode' in address:
            return address['postalCode']
        else:
            return None

    def creation_date(self, item: dict) -> Optional[str]:
        """Get creation date"""
        if item["creationDate"]:
            return item["creationDate"].split("T")[0]
        else:
            return None

    def registation_status(self, data: dict) -> str:
        """Get registation status"""
        return data["attributes"]["registration"]["status"]

    def entity_annotation(self, data: dict) -> Tuple[str, str]:
       """Annotation of status for all entity statements (not generated as a result
       of a reporting exception)"""
       lei = self.identifier(data)
       registration_status = self.registation_status(data)
       return (f"GLEIF data for this entity - LEI: {lei}; Registration Status: {registration_status}",
               "/")

    def subject_id(self, item: dict) -> str:
        """Get relationship subject identifier"""
        return item["attributes"]["relationship"]["startNode"]["id"]

    def interested_id(self, item: dict) -> str:
        """Get relationship interested party identifier"""
        return item["attributes"]["relationship"]["endNode"]["id"]

    def relationship_type(self, item: dict) -> str:
        """Get relationship type"""
        return item["attributes"]["relationship"]["type"]

    def update_date(self, item: dict) -> str:
        """Get update date"""
        return item["attributes"]['registration']['lastUpdateDate']

    def interest_details(self, item: dict) -> str:
        """Get interest details"""
        return f"LEI RelationshipType: {relationship_type(item)}"

    def interest_start_date(self, item: dict) -> str:
        """Get interest start date"""
        start_date = False
        if 'RelationshipPeriods' in data['Relationship']:
            periods = data['Relationship']['RelationshipPeriods']
            for period in periods:
                if 'StartDate' in period and 'PeriodType' in period:
                    if period['PeriodType'] == "RELATIONSHIP_PERIOD":
                        interestStartDate = period['StartDate']
                    else:
                        start_date = period['StartDate']
        if not start_date:
            if not interestStartDate: interestStartDate = ""
        else:
            if not interestStartDate: interestStartDate = start_date
        return interestStartDate

    def extract_links(self, data: dict) -> dict:
        """Extract links"""
        rel_links = {}
        item = extract_item(data)
        for rel in item["relationships"]:
            if rel.endswith("parent"):
                rel_type = rel.split("-")[0]
                if "reporting-exception" in item["relationships"][rel]["links"]:
                    rel_links[rel_type] = item["relationships"][rel]["links"]["reporting-exception"]
                else:
                    rel_links[rel_type] = item["relationships"][rel]["links"]["relationship-record"]
        return rel_links
