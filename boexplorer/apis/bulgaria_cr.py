import re
from datetime import datetime
from typing import Optional, Tuple, Union

from parsel import Selector

from boexplorer.apis.protocol import API
from boexplorer.utils.text import to_local_script


class BulgarianCR(API):
    """Handle accessing Bulgarian CR api"""

    @property
    def authenticator(self) -> str:
        """API authenticator"""
        return None

    @property
    def base_url(self) -> str:
        """API base url"""
        return "https://portal.registryagency.bg/CR/api/Deeds"

    @property
    def http_timeout(self) -> int:
        """API http method"""
        return 15

    @property
    def http_post(self) -> dict:
        """API http post"""
        return {"company_search": False,
                "company_detail": False,
                "company_persons": None,
                "person_search": False,
                "person_detail": None}

    @property
    def return_json(self) -> dict:
        """API returns json"""
        return {"company_search": True,
                "company_detail": True,
                "company_persons": None,
                "person_search": True,
                "person_detail": None}

    @property
    def post_pagination(self) -> bool:
        """API post pagination"""
        return False

    @property
    def company_search_url(self) -> str:
        """API company search url"""
        return f"{self.base_url}/Summary"

    def company_detail_url(self, company_data) -> str:
        """API company detail url"""
        return f"{self.base_url}/{company_data['ident']}"

    def company_persons_url(self, company_data) -> str:
        """API company detail url"""
        return "https://portal.registryagency.bg/CR/api/Deeds/SubjectInFields"

    @property
    def person_search_url(self) -> str:
        """API person search url"""
        return "https://portal.registryagency.bg/CR/api/Deeds/Subjects"

    def person_detail_url(self, company_data) -> str:
        """API company detail url"""
        return None

    def to_local_characters(self, text):
        """Transliterate into local cahracters"""
        return to_local_script(text, "bg")

    def from_local_characters(self, text):
        """Transliterate from local cahracters"""
        return to_local_script(text, "bg", reverse=True)

    @property
    def page_size_par(self) -> Tuple[str, bool]:
        """Page size parameter"""
        return "pageSize", False

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
        return {"name": text}

    @property
    def query_company_name_extra(self) -> str:
        """Querying company name extra parameters"""
        return {"selectedSearchFilter": 1}

    def query_company_detail_params(self, company_data) -> dict:
        """Querying company detail parameters"""
        return {}

    @property
    def query_company_detail_extra(self) -> str:
        """Querying company details extra parameters"""
        return {"entryDate": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                "loadFieldsFromAllLegalForms": "true"}

    def query_person_name_params(self, text) -> dict:
        """Querying person name parameter"""
        return {"page": 1,
                "pageSize": 25,
                "name": text,
                "selectedSearchFilter": 0}

    @property
    def query_person_name_extra(self) -> str:
        """Querying person name extra parameters"""
        return None

    def query_person_detail_params(self, person_data) -> dict:
        """Querying company detail parameters"""
        return None

    @property
    def query_person_detail_extra(self) -> str:
        """Querying company details extra parameters"""
        return None

    def check_result(self, json_data: Union[dict, list], detail=False) -> bool:
        """Check successful return value"""
        if detail:
            if isinstance(json_data, dict) and "companyName" in json_data:
                return True
            else:
                return False
        else:
            if isinstance(json_data, list):
                return True
            else:
                if 'code' in json_data:
                    print(f"Error: {json_data['code']} {json_data['message']}")
                return False

    def filter_result(self, data: dict, search=None, detail=False) -> bool:
        """Filter out item if meets condition"""
        return False

    def extract_data(self, json_data: dict) -> dict:
        """Extract main data body from json data"""
        return json_data

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

    def person_prepocessing(self, data: dict) -> dict:
        self.pre_processed = None

    def extract_type(self, json_data: dict) -> Optional[str]:
        """Extract item type (entity, relationship or exception)"""
        if "companyName" in json_data:
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

    def extract_relationship_item(self, data: dict) -> dict:
        """Extract relationship item data"""
        return data['attributes']['relationship']

    def identifier(self, data: dict) -> str:
        """Get entity identifier"""
        return data["uic"]

    def person_identifier(self, data: dict) -> str:
        """Get person identifier"""
        name = data['name'].strip().replace(' ', '-')
        return f"BG-EIK-PER-{name}"

    def entity_name(self, item: dict) -> str:
        """Get entity name"""
        return item["companyName"]

    def jurisdiction(self, item: dict) -> str:
        """Get jurisdiction"""
        return "BG"

    @property
    def scheme(self) -> str:
        """Get scheme"""
        return 'BG-EIK'

    @property
    def search_url(self) -> str:
        return 'https://portal.registryagency.bg/CR/en/Reports/VerificationPersonOrg'

    @property
    def scheme_name(self) -> str:
        """Get scheme name"""
        return 'Commercial Register (Bulgaria)'

    def additional_identifiers(self, item: dict) -> list:
        """Get list of additional identifiers"""
        return []

    def record_id(self, item: dict) -> str:
        """Get recordID"""
        if 'uic' in item:
            return f"BG-EIK-{item['uic']}"
        else:
            return self.person_identifier(item)

    def _extract_address(self) -> dict:
        if hasattr(self, "pre_processed"):
            address_data = self.pre_processed['CR_F_5_L']['text']
            next_data = address_data.split('Държава:')
            next_data = next_data[-1].split('Област:')
            country = next_data[0].strip()
            next_data = next_data[-1].split('Община:')
            district = next_data[0].strip()
            next_data = next_data[-1].split('място:')
            municipality = next_data[0].strip()
            next_data = next_data[-1].split('Телефон:')
            address = next_data[0].strip()
            next_data = next_data[-1].split('Факс:')
            telephone = next_data[0].strip()
            fax = next_data[-1].strip()
            return {'country': country,
                'district': district,
                'municipality': municipality,
                'address': address,
                'telephone': telephone,
                'fax': fax}
        else:
            return {'country': None,
                    'district': None,
                    'municipality': None,
                    'address': None,
                    'telephone': None,
                    'fax': None}

    def registered_address(self, item: dict) -> dict:
        """Get registered address"""
        address = self._extract_address()
        return address

    def business_address(self, item: dict) -> dict:
        """Get registered address"""
        address = self._extract_address()
        return address

    def person_address(self, item: dict) -> dict:
        """Get person address"""
        return item

    def source_type(self, data: dict) -> str:
        """Get source type"""
        return ['officialRegister']

    @property
    def source_description(self) -> str:
        """Get source description"""
        return 'Bulgaria (Commercial Register)'

    def address_string(self, address: dict) -> str:
        """Get address string"""
        address = self._extract_address()
        return address['address']

    def address_country(self, address: dict) -> str:
        """Get address country"""
        address = self._extract_address()
        if address['country'] == "БЪЛГАРИЯ":
            return "BG"
        else:
            return address['country']

    def address_postcode(self, address: dict) -> Optional[str]:
        """Get address postcode"""
        address = self._extract_address()
        match = re.findall("[0-9]{4}", address['address'])
        if match:
            return match[0]
        else:
            return None

    def _extract_creation_data(self) -> dict:
        creation_data = self.pre_processed['CR_F_1_L']['date']
        return creation_data

    def creation_date(self, item: dict) -> Optional[str]:
        """Get creation date"""
        creation_date = self._extract_creation_data()
        if creation_date:
            return creation_date.split("T")[0]
        else:
            return None

    def registation_status(self, data: dict) -> str:
        """Get registation status"""
        #return data["attributes"]["registration"]["status"]
        return None

    def entity_annotation(self, data: dict) -> Tuple[str, str]:
        """Annotation of status for all entity statements (not generated as a result
        of a reporting exception)"""
        lei = self.identifier(data)
        registration_status = self.registation_status(data)
        return (f"GLEIF data for this entity - LEI: {lei}; Registration Status: {registration_status}",
               "/")

    def person_annotation(self, data: dict) -> Tuple[str, str]:
        """Annotation of status for all person statements (not generated as a result of a reporting exception)"""
        ident = self.person_identifier(data)
        #registration_status = self.registation_status(data)
        return (f"Bulgarian EIK data for this person: {ident}", "/")

    def person_name_components(self, item: dict) -> Tuple[str, str, str, str]:
        """Extract person name components"""
        names = item["name"].split()
        famliy_name = names[-1]
        first_name = names[0]
        return item["name"], famliy_name, first_name, None

    def person_birth_date(self, item: dict):
        """Extract person birth date"""
        return None

    def person_tax_residency(self, item: dict):
        """Extract person tax residency"""
        if "taxResidencyOrJurisdiction" in item and item["taxResidencyOrJurisdiction"]:
            return item["taxResidencyOrJurisdiction"]
        else:
            return None

    def unspecified_person(self, item: dict):
        """Person unspecified"""
        if 'name' in item and item['name']:
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
        if not hasattr(self, "pre_processed"):
            return datetime.now().strftime("%Y-%m-%d")
        else:
            dates = [self.pre_processed[field]['date'].split("T")[0] for field in self.pre_processed]
            updated = sorted(dates, key=lambda d: datetime.strptime(d, "%Y-%m-%d"))[-1]
            return updated

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
