from thefuzz import fuzz
from typing import Optional, Tuple, Union

from boexplorer.apis.protocol import API
from boexplorer.data.data import lookup_scheme
from boexplorer.transforms.utils import current_date_iso

class LatviaUR(API):
    """Handle accessing Latvian UR api"""

    @property
    def authenticator(self) -> str:
        """API authenticator"""
        return None

    @property
    def base_url(self) -> str:
        """API base url"""
        return "https://info.ur.gov.lv/api"

    @property
    def http_timeout(self) -> int:
        """API http method"""
        return 15

    @property
    def http_headers(self):
        return None

    @property
    def http_post(self) -> dict:
        """API http post"""
        return {"company_search": False,
                "company_detail": None,
                "company_persons": False,
                "person_search": None,
                "person_detail": None}

    @property
    def return_json(self) -> dict:
        """API returns json"""
        return {"company_search": True,
                "company_detail": None,
                "company_persons": True,
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
        return f"{self.base_url}/legalentity/search"

    def company_detail_url(self, company_data) -> str:
        """API company detail url"""
        return None

    def company_persons_url(self, company_data: dict) -> str:
        """API company persons url"""
        if "code" in company_data:
            code = company_data["code"]
            return f"{self.base_url}/legalentity/api/{code}/persons/beneficiaries"
        else:
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
        return "pageSize", False

    @property
    def page_number_par(self) -> Tuple[str, int]:
        """Page number parameter"""
        return "page", 0

    @property
    def page_size_max(self) -> int:
        """Maximum page size"""
        return 25

    def query_company_name_params(self, text: str) -> dict:
        """Querying company name parameter"""
        return {"q": text}

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

    def query_company_persons_params(self, company_data) -> dict:
        """Querying company name parameter"""
        return {"lang": "LV", "fillForeignerData": True}

    def query_person_name_params(self, text) -> dict:
        """Querying person name parameter"""
        return None

    @property
    def query_person_name_extra(self) -> str:
        """Querying person name extra parameters"""
        return None

    def query_person_detail_params(self, company_data) -> dict:
        """Querying person detail parameters"""
        return None

    @property
    def query_person_detail_extra(self) -> str:
        """Querying person details extra parameters"""
        return None

    def check_result(self, json_data: Union[dict, list]) -> bool:
        """Check successful return value"""
        if isinstance(json_data, dict) and "responseHeader" in json_data:
            return True
        else:
            #if 'code' in json_data:
            #    print(f"Error: {json_data['code']} {json_data['message']}")
            return False

    def filter_result(self, data: dict, search_type=None, search=None, detail=False) -> bool:
        """Filter out item if meets condition"""
        #print("Filter:", search, data['name'] if 'name' in data else None)
        if search and data['name']:
            #print(data['name'], fuzz.ratio(search, data['name']))
            if fuzz.ratio(search, data['name']) > 50:
                return False
            else:
                return True
        else:
            return False

    def extract_data(self, json_data: dict) -> dict:
        """Extract main data body from json data"""
        return json_data["response"]["docs"]

    def extract_type(self, json_data: dict) -> Optional[str]:
        """Extract item type (entity, relationship or exception)"""
        if json_data["type"] == "lventity":
            return "entity"
        elif json_data["data"]["type"] == "relationship-records":
            return "relationship"
        elif json_data["data"]["type"] == "reporting-exceptions":
            return "exception"
        return None

    def extract_entity_item(self, data: dict) -> dict:
        """Extract entity item data"""
        return data

    def extract_person_item(self, data: dict) -> dict:
        """Extract person item data"""
        return data

    def extract_entity_persons_items(self, data: dict) -> dict:
        """Extract entity person item data"""
        if "records" in data:
            return data["records"]
        else:
            return []
        #items = []
        #if "kuvPersonsInfo" in data and data["kuvPersonsInfo"]:
        #    for item in data["kuvPersonsInfo"]:
        #        items.append(item)
        #return items

    def extract_relationship_item(self, data: dict) -> dict:
        """Extract relationship item data"""
        return data['attributes']['relationship']

    def identifier(self, data: dict) -> str:
        """Get entity identifier"""
        return data["regnumber"]

    def person_identifier(self, data: dict) -> str:
        """Get person identifier"""
        if "personCode" in data:
            ident = data["personCode"]
            return f"PL-ORSR-PER-{ident}"
        else:
            names = f'{data["firstname"]}-{data["lastname"]}'
            return f"PL-ORSR-PER-{names}"

    def entity_name(self, item: dict) -> str:
        """Get entity name"""
        return item['name']

    def jurisdiction(self, item: dict) -> str:
        """Get jurisdiction"""
        return "LV"

    @property
    def scheme(self) -> str:
        """Get scheme"""
        return "LV-RE"

    @property
    def search_url(self) -> str:
        """URL for manual search"""
        return 'https://info.ur.gov.lv/#/data-search'

    @property
    def scheme_name(self) -> str:
        """Get scheme name"""
        return "Commerce Register"

    def additional_identifiers(self, item: dict) -> list:
        """Get list of additional identifiers"""
        return []

    def record_id(self, item: dict) -> str:
        """Get recordID"""
        if 'regnumber' in item:
            return f"LV-RE-{item['regnumber']}"
        else:
            return self.person_identifier(item)

    def registered_address(self, item: dict) -> dict:
        """Get registered address"""
        return item

    def business_address(self, item: dict) -> dict:
        """Get registered address"""
        return None

    def person_address(self, item: dict) -> dict:
        """Get person address"""
        return None

    def source_type(self, data: dict) -> str:
        """Get source type"""
        return ['officialRegister']

    @property
    def source_description(self) -> str:
        """Get source description"""
        return "Commerce Register (Latvia)"

    def address_string(self, address: dict) -> str:
        """Get address string"""
        #lines = address['addressLines'] + [address['city']]
        #return ", ".join(lines)
        return address["address"]

    def address_country(self, address: dict) -> str:
        """Get address country"""
        return 'Latvia'

    def address_postcode(self, address: dict) -> Optional[str]:
        """Get address postcode"""
        if 'PostalCode' in address:
            return address['postalCode']
        else:
            return None

    def creation_date(self, item: dict) -> Optional[str]:
        """Get creation date"""
        if "registration_date" in item and item["registration_date"]:
            return item["registration_date"].split("T")[0]
        else:
            return None

    def registation_status(self, data: dict) -> str:
        """Get registation status"""
        return data["status"]

    def entity_annotation(self, data: dict) -> Tuple[str, str]:
       """Annotation of status for all entity statements (not generated as a result
       of a reporting exception)"""
       lei = self.identifier(data)
       registration_status = self.registation_status(data)
       return (f"Latvian Commerce Register data for this entity: {lei}; Registration Status: {registration_status}",
               "/")

    def person_annotation(self, data: dict) -> Tuple[str, str]:
        """Annotation of status for all person statements"""
        ident = self.person_identifier(data)
        return (f"Latvian Commerce Register data for this person: {ident}", "/")

    def person_name_components(self, item: dict) -> Tuple[str, str, str, str]:
        """Extract person name components"""
        family_name = item["lastname"]
        first_name = item["firstname"]
        names = f'{item["firstname"]} {item["lastname"]}'
        return names, family_name, first_name, None

    def person_birth_date(self, item: dict):
        """Extract person birth date"""
        return item["birthDate"].split("T")[0]

    def person_tax_residency(self, item: dict):
        """Extract person tax residency"""
        if "country" in item and item["country"]["value"]:
            return item["country"]["value"]
        else:
            return None

    def unspecified_person(self, item: dict):
        """Person unspecified"""
        if ("lastname" in item and item["lastname"]):
                return None
        return True

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
        return current_date_iso()

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
