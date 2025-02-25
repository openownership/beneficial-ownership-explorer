import re
from typing import Optional, Tuple, Union, List

from parsel import Selector

from boexplorer.apis.protocol import API
from boexplorer.utils.dates import current_date
from boexplorer.download.authentication import authenticator

class SlovakiaORSR(API):
    """Handle accessing Slovakia ORSR api"""

    @property
    def authenticator(self) -> str:
        """API authenticator"""
        return None

    @property
    def base_url(self) -> str:
        """API base url"""
        return "https://api.statistics.sk/rpo/v1"

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
                "person_search": False,
                "person_detail": None}
    @property
    def return_json(self) -> dict:
        """API returns json"""
        return {"company_search": True,
                "company_detail": None,
                "company_persons": True,
                "person_search": True,
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
        return f"{self.base_url}/search"

    def company_detail_url(self, company_data) -> str:
        """API company detail url"""
        return None

    def company_persons_url(self, company_data) -> str:
        """API company detail url"""
        identifier = company_data['id']
        return f"{self.base_url}/entity/{identifier}"

    @property
    def person_search_url(self) -> str:
        """API person search url"""
        return f"{self.base_url}/search"

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
        return {"fullName": text}

    @property
    def query_company_name_extra(self) -> str:
        """Querying company name extra parameters"""
        return {}

    def query_company_detail_params(self, company_data) -> dict:
        """Querying company detail parameters"""
        return {}

    @property
    def query_company_detail_extra(self) -> str:
        """Querying company details extra parameters"""
        return None

    def query_company_persons_params(self, company_data) -> dict:
        """Querying company name parameter"""
        return {"showHistoricalData": True}

    def query_person_name_params(self, text) -> dict:
        """Querying person name parameters"""
        return {"fullName": text}

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
            if isinstance(json_data, dict) and "results" in json_data:
                return True
            else:
                return False
        else:
            if "results" in json_data:
                return True
            else:
                return False

    def _is_person(self, data: dict):
       if 'personName' in data:
           return True
       else:
            if data["sourceRegister"]["value"]["code"] == "2":
                return True
            else:
                return False

    def filter_result(self, data: dict, search_type=None, search=None, detail=False) -> bool:
        """Filter out item if meets condition"""
        if search_type == "person":
            if self._is_person(data):
                return False
            else:
                return True
        else:
            return False

    def extract_data(self, json_data: dict) -> dict:
        """Extract main data body from json data"""
        return json_data["results"]

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
        if "establishment" in json_data:
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
        items = []
        if "kuvPersonsInfo" in data and data["kuvPersonsInfo"]:
            for item in data["kuvPersonsInfo"]:
                items.append(item)
        return items

    def extract_relationship_item(self, data: dict) -> dict:
        """Extract relationship item data"""
        return data['attributes']['relationship']

    def _extract_latest(self, items: List) -> dict:
        for item in items:
            if not "validTo" in item:
                return item
        return None

    def identifier(self, data: dict) -> str:
        """Get entity identifier"""
        latest = self._extract_latest(data["identifiers"])
        return latest["value"] if latest else None

    def person_identifier(self, data: dict) -> str:
        """Get person identifier"""
        if "personName" in data:
            names = data["personName"]["formatedName"].replace(" ", "-")
            return f"SK-ORSR-PER-{names}"
        else:
            #if "identifiers" in data and len(data["identifiers"]) > 0:
            #    ident = data["identifiers"][0]["value"]
            #    return f"PL-ORSR-PER-{ident}"
            #else:
            names = data["fullNames"][-1]["value"].replace(" ", "-")
            return f"SK-ORSR-PER-{names}"

    def entity_name(self, item: dict) -> str:
        """Get entity name"""
        latest = self._extract_latest(item["fullNames"])
        return latest["value"] if latest else None

    def jurisdiction(self, item: dict) -> str:
        """Get jurisdiction"""
        return "SK"

    @property
    def scheme(self) -> str:
        """Get scheme"""
        return "SK-ORSR"

    @property
    def search_url(self) -> str:
        """URL for manual search"""
        return 'https://www.orsr.sk/search_subjekt.asp?lan=en'

    @property
    def scheme_name(self) -> str:
        """Get scheme name"""
        return "Business Register"

    def additional_identifiers(self, item: dict) -> list:
        """Get list of additional identifiers"""
        return []

    def record_id(self, item: dict) -> str:
        """Get recordID"""
        if not self._is_person(item):
            identifier = self.identifier(item)
            return f"SK-ORSR-{identifier}"
        else:
            return self.person_identifier(item)

    def registered_address(self, item: dict) -> dict:
        """Get registered address"""
        if "addresses" in item and len(item["addresses"]) > 0:
            return item["addresses"][0]
        else:
            return None

    def business_address(self, item: dict) -> dict:
        """Get registered address"""
        return None

    def person_address(self, item: dict) -> dict:
        """Get person address"""
        if "addresses" in item and len(item["addresses"]) > 0:
            return item["addresses"]
        else:
            return None

    def source_type(self, data: dict) -> str:
        """Get source type"""
        return ['officialRegister']

    @property
    def source_description(self) -> str:
        """Get source description"""
        return 'Business Register (SK)'

    def address_string(self, address: dict) -> str:
        """Get address string"""
        if address:
            if isinstance(address, list):
                address = address[-1]
            print(address)
            address_data = []
            if "buildingNumber" in address and address["buildingNumber"]:
                address_data.append(address["buildingNumber"])
            if "street" in address and address["street"]:
                address_data.append(address["street"])
            if "municipality" in address and address["municipality"]["value"]:
                address_data.append(address["municipality"]["value"])
            if "postalCodes" in address and len(address["postalCodes"]) > 0:
                address_data.append(address["postalCodes"][0])
            #return f"{address_data[1]} {address_data[0]}, {address_data[2]} {address_data[3]}"
            return f"{address_data[0]} {', '.join(address_data[1:])}"
        else:
            return None

    def address_country(self, address: dict) -> str:
        """Get address country"""
        if isinstance(address, list):
            address = address[-1]
        return address['country']['value'] if "country" in address else None

    def address_postcode(self, address: dict) -> Optional[str]:
        """Get address postcode"""
        if isinstance(address, list):
            address = address[-1]
        return address["postalCodes"] if ("postalCodes" in address and
                                          len(address["postalCodes"]) > 0) else None

    def creation_date(self, item: dict) -> Optional[str]:
        """Get creation date"""
        creation_date = item["establishment"] if "establishment" in item else None
        if creation_date:
            return creation_date.split("T")[0]
        else:
            return None

    def registation_status(self, data: dict) -> str:
        """Get registation status"""
        return "Active" if not "termination" in data else "Terminated"

    def entity_annotation(self, data: dict) -> Tuple[str, str]:
       """Annotation of status for all entity statements (not generated as a result
       of a reporting exception)"""
       ident = self.identifier(data)
       registration_status = self.registation_status(data)
       return (f"Slokavian Business Register data for this entity: {ident}; Registration Status: {registration_status}",
               "/")

    def person_annotation(self, data: dict) -> Tuple[str, str]:
        """Annotation of status for all person statements (not generated as a result of a reporting exception)"""
        ident = self.person_identifier(data)
        #registration_status = self.registation_status(data)
        return (f"Slokavian Business Register data for this person: {ident}", "/")

    def person_name_components(self, item: dict) -> Tuple[str, str, str, str]:
        """Extract person name components"""
        if "personName" in item:
            family_name = item["personName"]["familyNames"]
            middle_name = None
            first_name = item["personName"]["givenNames"]
            names = item["personName"]["formatedName"]
            return names, family_name, first_name, None
        else:
            names = item["fullNames"][-1]["value"]
            family_name = names.split()[-1]
            first_name = names.split()[0]
            return names, family_name, first_name, None

    def person_birth_date(self, item: dict):
        """Extract person birth date"""
        return None

    def person_tax_residency(self, item: dict):
        """Extract person tax residency"""
        if "country" in item and item["country"]["value"]:
            return item["country"]["value"]
        else:
            return None

    def unspecified_person(self, item: dict):
        """Person unspecified"""
        if ("personName" in item and item["personName"]) or ("fullNames" in item and len(item["fullNames"]) > 0):
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
