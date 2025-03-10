import re
from typing import Optional, Tuple, Union

from parsel import Selector

from boexplorer.apis.protocol import API
from boexplorer.utils.dates import current_date
from boexplorer.download.authentication import authenticator
from boexplorer.download.stealth import  session_cookie

class DenmarkCVR(API):
    """Handle accessing Danish CVR api"""

    @property
    def authenticator(self) -> str:
        """API authenticator"""
        return None

    @property
    def base_url(self) -> str:
        """API base url"""
        return 'https://datacvr.virk.dk/gateway/soeg/fritekst'

    @property
    def http_timeout(self) -> int:
        """API http method"""
        return 15

    @property
    def http_headers(self):
        return {"Accept": "application/json, text/plain, */*",
                "Accept-Encoding": "gzip, deflate, br, zstd",
                "Accept-Language": "en-GB,en;q=0.8",
                "Cache-Control": "no-cache",
                #"Content-Length": 325,
                #"Content-Type": "application/json",
                "Origin": "https://datacvr.virk.dk",
                "Priority": "u=1, i",
                "Referer": "https://datacvr.virk.dk/soegeresultater?fritekst=Harings&sideIndex=0&size=10",
                "Sec-Ch-Ua": '"Not)A;Brand";v="99", "Brave";v="127", "Chromium";v="127"',
                "Sec-Ch-Ua-Mobile": "?0",
                "Sec-Ch-Ua-Platform": "Linux",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
                "Sec-Gpc": "1",
                "X-Requested-With": "XMLHttpRequest"}

    @property
    def http_post(self) -> dict:
        """API http post"""
        return {"company_search": True,
                "company_detail": None,
                "company_persons": None,
                "person_search": True,
                "person_detail": None}

    @property
    def return_json(self) -> dict:
        """API returns json"""
        return {"company_search": True,
                "company_detail": None,
                "company_persons": None,
                "person_search": True,
                "person_detail": None}

    @property
    def post_pagination(self) -> bool:
        """API post pagination"""
        return True

    @property
    def session_cookie(self):
        user_agent, cookie = session_cookie("https://datacvr.virk.dk", 'S9SESSIONID')
        return user_agent, cookie

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
        return f"{self.base_url}"

    def person_detail_url(self, company_data) -> str:
        """API company detail url"""
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
        return "size", True

    @property
    def page_number_par(self) -> Tuple[str, int]:
        """Page number parameter"""
        return "sideIndex", 0

    @property
    def page_size_max(self) -> int:
        """Maximum page size"""
        return 10

    def query_company_name_params(self, text) -> dict:
        """Querying company name parameter"""
        return {"fritekstCommand": {"enhedstype": "virksomhed",
                                    "soegOrd": text,
                                    "antalAnsatte": [],
                                    "branchekode": "",
                                    "kommune": [],
                                    "ophoersdatoFra": "",
                                    "ophoersdatoTil": "",
                                    "personrolle": [],
                                    "region": [],
                                    "sortering": "",
                                    "startdatoFra": "",
                                    "startdatoTil": "",
                                    "virksomhedsform": [],
                                    "virksomhedsmarkering": [],
                                    "virksomhedsstatus": []
                                    }
               }

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
        return {"fritekstCommand": {"antalAnsatte": [],
                                  "branchekode": "",
                                  "enhedstype": "person",
                                  "kommune": [],
                                  "ophoersdatoFra": "",
                                  "ophoersdatoTil": "",
                                  "personrolle": [],
                                  "region": [],
                                  "sideIndex": "0",
                                  "size": ["10"],
                                  "soegOrd": text,
                                  "sortering": "",
                                  "startdatoFra": "",
                                  "startdatoTil": "",
                                  "virksomhedsform": [],
                                  "virksomhedsmarkering": [],
                                  "virksomhedsstatus": []}}

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
            if "enheder" in json_data:
                return True
            else:
                return False

    def filter_result(self, data: dict, search_type=None, search=None, detail=False) -> bool:
        """Filter out item if meets condition"""
        return False

    def extract_data(self, json_data: dict) -> dict:
        """Extract main data body from json data"""
        if "enheder" in json_data:
            return json_data["enheder"]
        else:
            return []

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
        if "enhedstype" in json_data and json_data["enhedstype"] == "virksomhed":
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
        return data['cvr']

    def person_identifier(self, data: dict) -> str:
        """Get person identifier"""
        #if "senesteNavn" in item:
        #if 'affiliatesFirstname' in data and data['affiliatesFirstname']:
        #    name = f"{data['affiliatesFirstname'].strip()}-{data['affiliatesSurname'].strip().replace(' ', '-')}"
        #    address_number = data['affiliatesStreetNumber'].strip().split()[-1:] if data['affiliatesStreetNumber'].strip() else []
        #    address_components = address_number + data["affiliatesAddress"].strip().split()
        #    first_comps = []
        #    last_comp = None
        #    for comp in address_components:
        #        if comp:
        #            if not last_comp or (comp != last_comp):
        #                first_comps.append(comp)
        #    #address_components = [comp for comp in address_components if comp]
        #    address = f"{first_comps[0]}-{first_comps[1]}"
        #    return f"NG-CAC-BOR-{name}-{address}"
        #else:
        return f"DK-CVR-PER-{data['enhedsnummer']}"

    def entity_name(self, item: dict) -> str:
        """Get entity name"""
        return item["senesteNavn"]

    def jurisdiction(self, item: dict) -> str:
        """Get jurisdiction"""
        return "DK"

    @property
    def scheme(self) -> str:
        """Get scheme"""
        return "DK-CVR"

    @property
    def search_url(self) -> str:
        return 'https://datacvr.virk.dk/'

    @property
    def scheme_name(self) -> str:
        """Get scheme name"""
        return "Central Business Register"

    def additional_identifiers(self, item: dict) -> list:
        """Get list of additional identifiers"""
        return []

    def record_id(self, item: dict) -> str:
        """Get recordID"""
        if 'cvr' in item:
            return f"DK-CVR-{item['cvr']}"
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
        return item

    def source_type(self, data: dict) -> str:
        """Get source type"""
        return ['officialRegister']

    @property
    def source_description(self) -> str:
        """Get source description"""
        return "Central Business Register (DK)"

    def address_string(self, address: dict) -> str:
        """Get address string"""
        if address:
            address_data = []
            if  "beliggenhedsadresse" in address and address["beliggenhedsadresse"]:
                address_data.append(address["beliggenhedsadresse"])
            if "by" in address and address["by"]:
                address_data.append(address["by"])
            #if "region" in address and address["region"]:
            #    address_data.append(address["region"])
            return ", ".join(address_data)
        else:
            return None

    def address_country(self, address: dict) -> str:
        """Get address country"""
        return address['country'] if "country" in address else None

    def address_postcode(self, address: dict) -> Optional[str]:
        """Get address postcode"""
        return address["postnummer"]

    def creation_date(self, item: dict) -> Optional[str]:
        """Get creation date"""
        creation_date = item["startDato"]
        if creation_date:
            return creation_date.split("T")[0]
        else:
            return None

    def registation_status(self, data: dict) -> str:
        """Get registation status"""
        if data["status"]== "Oph\u00f8rt":
            return "Ceased"
        elif data["status"] == "Aktiv":
            return "Active"
        return None

    def entity_annotation(self, data: dict) -> Tuple[str, str]:
        """Annotation of status for all entity statements (not generated as a result
        of a reporting exception)"""
        ident = self.identifier(data)
        registration_status = self.registation_status(data)
        return (f"DK Central Business Register data for this entity: {ident}; Registration Status: {registration_status}",
               "/")

    def person_annotation(self, data: dict) -> Tuple[str, str]:
        """Annotation of status for all entity statements (not generated as a result
        of a reporting exception)"""
        ident = self.person_identifier(data)
        #registration_status = self.registation_status(data)
        return (f"DK Central Business Register data for this person: {ident}",
               "/")
    def person_name_components(self, item: dict) -> Tuple[str, str, str, str]:
        """Extract person name components"""
        names = item["senesteNavn"].split()
        famliy_name = names[-1]
        first_name = names[0]
        return item["senesteNavn"], famliy_name, first_name, None

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
        if "senesteNavn" in item and item["senesteNavn"]:
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
