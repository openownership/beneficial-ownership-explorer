import re
from typing import Optional, Tuple, Union

from parsel import Selector

from boexplorer.apis.protocol import API
from boexplorer.utils.dates import current_date
from boexplorer.download.authentication import authenticator
from boexplorer.config import app_config

class UKPSC(API):
    """Handle accessing UK PSC api"""

    @property
    def authenticator(self) -> str:
        """API authenticator"""
        return authenticator(app_config["sources"]["uk_psc"]["credentials"]["user"],
                             app_config["sources"]["uk_psc"]["credentials"]["pass"])

    @property
    def base_url(self) -> str:
        """API base url"""
        return "https://api.company-information.service.gov.uk/advanced-search/companies"

    @property
    def http_timeout(self) -> int:
        """API http timeout (seconds)"""
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
        return f"{self.base_url}"

    def company_detail_url(self, company_data) -> str:
        """API company detail url"""
        return None

    def company_persons_url(self, company_data) -> str:
        """API company detail url"""
        company_number = company_data['company_number']
        return f"https://api.company-information.service.gov.uk/company/{company_number}/persons-with-significant-control"

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
        return "limit", False

    @property
    def page_number_par(self) -> Tuple[str, int]:
        """Page number parameter"""
        return "page", 1

    @property
    def page_size_max(self) -> int:
        """Maximum page size"""
        return 25

    def query_company_name_params(self, text) -> dict:
        """Querying company name parameter"""
        return {"company_name_includes": text}

    @property
    def query_company_name_extra(self) -> str:
        """Querying company name extra parameters"""
        return {}

    def query_company_detail_params(self, company_data) -> dict:
        """Querying company detail parameters"""
        #return {"id": company_data["companyId"]}
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

    def query_company_persons_params(self, company_data) -> dict:
        """Querying company name parameter"""
        return {}

    def query_person_name_params(self, company_data) -> dict:
        """Querying person name parameters"""
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

    def check_result(self, json_data: Union[dict, list], detail=False) -> bool:
        """Check successful return value"""
        if detail:
            if isinstance(json_data, dict) and "companyName" in json_data:
                return True
            else:
                return False
        else:
            if "etag" in json_data:
                return True
            else:
                return False

    def filter_result(self, data: dict, search_type=None, search=None, detail=False) -> bool:
        """Filter out item if meets condition"""
        if not "company_number" in data:
            if data['kind'] == 'individual-person-with-significant-control':
                return False
            else:
                return True
        else:
            return False

    def extract_data(self, json_data: dict) -> dict:
        """Extract main data body from json data"""
        return json_data['items']

    def company_prepocessing(self, data: dict) -> dict:
        self.pre_processed = {}
        for section in data["sections"]:
            section_name = section["nameCode"]
            #self.pre_processed[section_name] = {}
            for subdeed in section["subDeeds"]:
                subdeed_name = subdeed["sectionName"]
                #self.pre_processed[section_name][subdeed_name] = {}
                for group in subdeed["groups"]:
                    group_name = group["nameCode"]
                    #self.pre_processed[section_name][subdeed_name][group_name] = {}
                    for field in group["fields"]:
                        field_name = field["nameCode"]
                        selector = Selector(text=field["htmlData"])
                        text = " ".join(selector.xpath('//text()').getall())
                        latin = self.from_local_characters(text)
                        #self.pre_processed[section_name][subdeed_name][group_name][field_name] = {'text': text}
                        self.pre_processed[field_name] = {'text': text, 'date': field["fieldEntryDate"]}
                        print(f"{field_name}: {latin} {text}")
        print(self.pre_processed)

    def extract_type(self, json_data: dict) -> Optional[str]:
        """Extract item type (entity, relationship or exception)"""
        if "company_number" in json_data:
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
        print(data)
        return data["items"]

    def extract_relationship_item(self, data: dict) -> dict:
        """Extract relationship item data"""
        return data['attributes']['relationship']

    def identifier(self, data: dict) -> str:
        """Get entity identifier"""
        return data['company_number']

    def person_identifier(self, data: dict) -> str:
        """Get person identifier"""
        names = data["name"].replace(" ", "-")
        return f"GB-COH-PER-{names}"

    def entity_name(self, item: dict) -> str:
        """Get entity name"""
        return item["company_name"]

    def jurisdiction(self, item: dict) -> str:
        """Get jurisdiction"""
        return "UK"

    @property
    def scheme(self) -> str:
        """Get scheme"""
        return 'GB-COH'

    @property
    def search_url(self) -> str:
        """URL for manual search"""
        return 'https://find-and-update.company-information.service.gov.uk/'

    @property
    def scheme_name(self) -> str:
        """Get scheme name"""
        return 'Companies House'

    def additional_identifiers(self, item: dict) -> list:
        """Get list of additional identifiers"""
        return []

    def record_id(self, item: dict) -> str:
        """Get recordID"""
        if 'company_number' in item:
            return f"GB-COH-{item['company_number']}"
        else:
            return self.person_identifier(item)

    def registered_address(self, item: dict) -> dict:
        """Get registered address"""
        return item["registered_office_address"]

    def business_address(self, item: dict) -> dict:
        """Get registered address"""
        return None

    def person_address(self, item: dict) -> dict:
        """Get person address"""
        return item['address']

    def source_type(self, data: dict) -> str:
        """Get source type"""
        return ['officialRegister']

    @property
    def source_description(self) -> str:
        """Get source description"""
        return 'Companies House (UK)'

    def address_string(self, address: dict) -> str:
        """Get address string"""
        if address:
            address_data = []
            if "address_line_1" in address and address["address_line_1"]:
                address_data.append(address["address_line_1"])
            if "address_line_2" in address and address["address_line_2"]:
                address_data.append(address["address_line_2"])
            if "locality" in address and address["locality"]:
                address_data.append(address["locality"])
            if "region" in address and address["region"]:
                address_data.append(address["region"])
            return ", ".join(address_data)
        else:
            return None

    def address_country(self, address: dict) -> str:
        """Get address country"""
        return address['country'] if "country" in address else None

    def address_postcode(self, address: dict) -> Optional[str]:
        """Get address postcode"""
        return address["postal_code"] if "postal_code" in address else None

    def creation_date(self, item: dict) -> Optional[str]:
        """Get creation date"""
        creation_date = item["date_of_creation"]
        if creation_date:
            return creation_date.split("T")[0]
        else:
            return None

    def registation_status(self, data: dict) -> str:
        """Get registation status"""
        #return data["attributes"]["registration"]["status"]
        return data["company_status"]

    def entity_annotation(self, data: dict) -> Tuple[str, str]:
       """Annotation of status for all entity statements"""
       ident = self.identifier(data)
       registration_status = self.registation_status(data)
       return (f"UK Companies House data for this entity: {ident}; Registration Status: {registration_status}",
               "/")

    def person_annotation(self, data: dict) -> Tuple[str, str]:
        """Annotation of status for all person statements"""
        ident = self.person_identifier(data)
        return (f"UK Companies House data for this person: {ident}", "/")

    def person_name_components(self, item: dict) -> Tuple[str, str, str, str]:
        """Extract person name components"""
        family_name = item["name_elements"]["surname"]
        #middle_name = item["name_elements"]["middle_name"]
        first_name = item["name_elements"]["forename"]
        return item["name"], family_name, first_name, None

    def person_birth_date(self, item: dict):
        """Extract person birth date"""
        month = item["date_of_birth"]["month"]
        year = item["date_of_birth"]["year"]
        return f"{year}-{month}"

    def person_tax_residency(self, item: dict):
        """Extract person tax residency"""
        if "country_of_residence" in item and item["country_of_residence"]:
            return item["country_of_residence"]
        else:
            return None

    def unspecified_person(self, item: dict):
        """Person unspecified"""
        if "name" in item and item["name"]:
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
        return current_date()

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
