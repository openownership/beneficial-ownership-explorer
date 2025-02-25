import re
from typing import Optional, Tuple, Union

from parsel import Selector

from boexplorer.apis.protocol import API
from boexplorer.utils.dates import current_date

class NigerianCAC(API):
    """Handle accessing Nigerian CAC api"""

    @property
    def authenticator(self) -> str:
        """API authenticator"""
        return None

    @property
    def base_url(self) -> str:
        """API base url"""
        #return "https://borapp.cac.gov.ng/borapp/api/bor-search"
        #return "https://searchapp.cac.gov.ng/searchapp/api/public/public-search/company-business-name-it"
        return "https://searchapp.cac.gov.ng/api/public/public-search/company-business-name-it"

    @property
    def http_timeout(self) -> int:
        """API http method"""
        return 90

    @property
    def http_headers(self):
        return None

    @property
    def http_post(self) -> dict:
        """API http method"""
        return {"company_search": True,
                "company_detail": None,
                "company_persons": None,
		"person_search": True,
                "person_detail": True}

    @property
    def return_json(self) -> dict:
        """API returns json"""
        return {"company_search": True,
                "company_detail": None,
                "company_persons": None,
                "person_search": True,
                "person_detail": True}

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

    @property
    def person_search_url(self) -> str:
        """API person search url"""
        return "https://borapp.cac.gov.ng/borapp/api/bor-search/get_psc"

    def person_detail_url(self, company_data) -> str:
        """API company detail url"""
        return "https://borapp.cac.gov.ng/borapp/api/bor-search/get_psc_details"

    def to_local_characters(self, text):
        """Transliterate into local characters"""
        return text

    def from_local_characters(self, text):
        """Transliterate from local characters"""
        return text

    @property
    def page_size_par(self) -> Tuple[str, bool]:
        """Page size parameter"""
        #return "limit", False
        #return None, False
        return "limit", False

    @property
    def page_number_par(self) -> Tuple[str, int]:
        """Page number parameter"""
        #return "page", 1
        #return None, 1
        return "page", 1

    @property
    def page_size_max(self) -> int:
        """Maximum page size"""
        return 25

    def query_company_name_params(self, text) -> dict:
        """Querying company name parameter"""
        return {"searchTerm": text} #, "classification": {"id": 2}}

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
        return {"searchItem": text, "searchType": "PSC FULLNAME"}

    @property
    def query_person_name_extra(self) -> str:
        """Querying person name extra parameters"""
        return None

    def query_person_detail_params(self, person_data) -> dict:
        """Querying company detail parameters"""
        return {"id": person_data["companyId"]}

    @property
    def query_person_detail_extra(self) -> str:
        """Querying company details extra parameters"""
        return None

    def check_result(self, json_data: Union[dict, list], detail=False) -> bool:
        """Check successful return value"""
        if detail:
            if isinstance(json_data, dict) and "companyName" in json_data:
                return True
            elif isinstance(json_data, list) and len(json_data) > 0 and "affiliatesFirstname" in json_data[0]:
                return True
            else:
                return False
        else:
            print(json_data)
            if json_data["status"] == "OK":
                return True
            else:
                return False

    def filter_result(self, data: dict, search_type=None, search=None, detail=False) -> bool:
        """Filter out item if meets condition"""
        if search_type == "person":
            if 'affiliatesSurname' in data and data['affiliatesSurname']:
                return False
            else:
                return True
        else:
            if 'rcNumber' in data and data['rcNumber']:
                return False
            else:
                return True
            #if "affiliateIsCorporate" in data and data["affiliateIsCorporate"]:
            #    return True
            #else:
            #    return False

    def extract_data(self, json_data: dict) -> dict:
        """Extract main data body from json data"""
        if isinstance(json_data, dict) and "data" in json_data and json_data['data']:
            return json_data['data']['data']
        elif isinstance(json_data, list):
            return json_data
        else:
            return None

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
        pass

    def extract_type(self, json_data: dict) -> Optional[str]:
        """Extract item type (entity, relationship or exception)"""
        if "rcNumber" in json_data:
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
        return f"RC{data['rcNumber']}"

    def person_identifier(self, data: dict) -> str:
        """Get person identifier"""
        if 'affiliatesFirstname' in data and data['affiliatesFirstname']:
            name = f"{data['affiliatesFirstname'].strip()}-{data['affiliatesSurname'].strip().replace(' ', '-')}"
            address_number = data['affiliatesStreetNumber'].strip().split()[-1:] if data['affiliatesStreetNumber'].strip() else []
            address_components = address_number + data["affiliatesAddress"].strip().split()
            first_comps = []
            last_comp = None
            for comp in address_components:
                if comp:
                    if not last_comp or (comp != last_comp):
                        first_comps.append(comp)
            #address_components = [comp for comp in address_components if comp]
            address = f"{first_comps[0]}-{first_comps[1]}"
            return f"NG-CAC-BOR-{name}-{address}"
        else:
            return f"NG-CAC-BOR-{data['id']}"

    def entity_name(self, item: dict) -> str:
        """Get entity name"""
        return item["approvedName"]

    def jurisdiction(self, item: dict) -> str:
        """Get jurisdiction"""
        return "NG"

    @property
    def scheme(self) -> str:
        """Get scheme"""
        return 'NG-CAC'

    @property
    def search_url(self) -> str:
        """URL for manual search"""
        #return 'https://search.cac.gov.ng/home'
        return 'https://bor.cac.gov.ng/'

    @property
    def scheme_name(self) -> str:
        """Get scheme name"""
        return 'Corporate Affairs Commission'

    def additional_identifiers(self, item: dict) -> list:
        """Get list of additional identifiers"""
        return []

    def record_id(self, item: dict) -> str:
        """Get recordID"""
        if not 'affiliatesSurname' in item:
            return f"NG-CAC-RC{item['rcNumber']}"
        else:
            ident = self.person_identifier(item)
            return ident

    def _extract_address(self, item) -> dict:
        if "affiliatesAddress" in item:
            return {'country': "NG",
                    'district': item["affiliatesState"],
                    'municipality': item["affiliatesCity"],
                    'address': " ".join([item["affiliatesStreetNumber"].strip(),
                                        item["affiliatesAddress"].strip()]).strip(),
                    'telephone': None,
                    'fax': None}
        else:
            return {'country': "NG",
                'district': None,
                'municipality': None,
                'address': None,
                'telephone': None,
                'fax': None}

    def registered_address(self, item: dict) -> dict:
        """Get registered address"""
        address = self._extract_address(item)
        return address

    def business_address(self, item: dict) -> dict:
        """Get registered address"""
        address = self._extract_address(item)
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
        return 'Corporate Affairs Commission (Nigeria)'

    def address_string(self, address: dict) -> str:
        """Get address string"""
        address = self._extract_address(address)
        return address['address']

    def address_country(self, address: dict) -> str:
        """Get address country"""
        address = self._extract_address(address)
        return address['country']

    def address_postcode(self, address: dict) -> Optional[str]:
        """Get address postcode"""
        if "affiliatesPostcode" in address:
            return address["affiliatesPostcode"]
        else:
            #address = self._extract_address()
            return None

    def creation_date(self, item: dict) -> Optional[str]:
        """Get creation date"""
        creation_date = item["registrationDate"]
        if creation_date:
            return creation_date.split("T")[0]
        else:
            return None

    def registation_status(self, data: dict) -> str:
        """Get registation status"""
        #return data["attributes"]["registration"]["status"]
        return data["status"]

    def entity_annotation(self, data: dict) -> Tuple[str, str]:
        """Annotation of status for all entity statements (not generated as a result
        of a reporting exception)"""
        ident = self.identifier(data)
        registration_status = self.registation_status(data)
        return (f"Nigerina CAC data for this entity: {ident}; Registration Status: {registration_status}",
               "/")

    def person_annotation(self, data: dict) -> Tuple[str, str]:
        """Annotation of status for all person statements (not generated as a result of a reporting exception)"""
        ident = self.person_identifier(data)
        #registration_status = self.registation_status(data)
        return (f"Nigerina CAC BOR data for this person: {ident}", "/")

    def person_name_components(self, item: dict) -> Tuple[str, str, str, str]:
        """Extract person name components"""
        famliy_name = item['affiliatesSurname']
        first_name = item['affiliatesFirstname']
        other_name = item['otherName']
        full_name = " ".join([name for name in (first_name, other_name, famliy_name) if name])
        return full_name, famliy_name, first_name, None

    def person_birth_date(self, item: dict):
        """Extract person birth date"""
        return item["dateOfBirth"]

    def person_tax_residency(self, item: dict):
        """Extract person tax residency"""
        if "taxResidencyOrJurisdiction" in item and item["taxResidencyOrJurisdiction"]:
            return item["taxResidencyOrJurisdiction"]
        else:
            return None

    def unspecified_person(self, item: dict):
        """Person unspecified"""
        for name in ('affiliatesFirstname', 'affiliatesSurname', 'otherName'):
            if name in item and item[name]:
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
