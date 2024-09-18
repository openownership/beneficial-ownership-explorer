import re
from typing import Optional, Tuple, Union

from parsel import Selector

from boexplorer.apis.protocol import API
from boexplorer.utils.dates import current_date
from boexplorer.download.authentication import authenticator

class PolandKRS(API):
    """Handle accessing Polish KRS api"""

    @property
    def authenticator(self) -> str:
        """API authenticator"""
        return None

    @property
    def base_url(self) -> str:
        """API base url"""
        return ""

    @property
    def http_post(self) -> dict:
        """API http post"""
        return {"company_search": True,
                "company_detail": False}

    @property
    def post_pagination(self) -> bool:
        """API post pagination"""
        return False

    @property
    def company_search_url(self) -> str:
        """API company search url"""
        return "https://prs-openapi2-prs-prod.apps.ocp.prod.ms.gov.pl/api/wyszukiwarka/krs"

    def company_detail_url(self, company_data) -> str:
        """API company detail url"""
        krs_number = f'{int(company_data["numer"]):010d}'
        return f"https://api-krs.ms.gov.pl/api/krs/OdpisAktualny/{krs_number}"

    def to_local_characters(self, text):
        """Transliterate into local characters"""
        return text

    def from_local_characters(self, text):
        """Transliterate from local characters"""
        return text

    @property
    def page_size_par(self) -> Tuple[str, bool]:
        """Page size parameter"""
        return False, False

    @property
    def page_number_par(self) -> Tuple[str, int]:
        """Page number parameter"""
        return False, 1

    @property
    def page_size_max(self) -> int:
        """Maximum page size"""
        return 100

    def query_company_name_params(self, text) -> dict:
        """Querying company name parameter"""
        return {"rejestr": ["P"],
                    "podmiot": {"krs": None,
                                "nip": None,
                                "regon": None,
                                "nazwa": text,
                                "wojewodztwo": None,
                                "powiat":"",
                                "gmina":"",
                                "miejscowosc":""},
                     "status": {"czyOpp": None,
                                "czyWpisDotyczacyPostepowaniaUpadlosciowego": None,
                                "dataPrzyznaniaStatutuOppOd": None,
                                "dataPrzyznaniaStatutuOppDo": None},
                     "paginacja": {"liczbaElementowNaStronie":100,
                                   "maksymalnaLiczbaWynikow":100,
                                   "numerStrony":1}}

    @property
    def query_company_name_extra(self) -> str:
        """Querying company name extra parameters"""
        return {}

    def query_company_detail_params(self, company_data) -> dict:
        """Querying company detail parameters"""
        return {"rejestr": "P", "format": "json"}

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

    def check_result(self, json_data: Union[dict, list], detail=False) -> bool:
        """Check successful return value"""
        if detail:
            if isinstance(json_data, dict) and "odpis" in json_data:
                return True
            else:
                return False
        else:
            if "listaPodmiotow" in json_data:
                return True
            else:
                return False

    def filter_result(self, data: dict, detail=False) -> bool:
        """Filter out item if meets condition"""
        return False

    def extract_data(self, json_data: dict) -> dict:
        """Extract main data body from json data"""
        return json_data["listaPodmiotow"]

    def company_prepocessing(self, data: dict) -> dict:
        return data["odpis"]

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

    def extract_relationship_item(self, data: dict) -> dict:
        """Extract relationship item data"""
        return data['attributes']['relationship']

    def indentifier(self, data: dict) -> str:
        """Get entity identifier"""
        return f'{int(data["odpis"]["naglowekA"]["numerKRS"]):010d}'

    def entity_name(self, item: dict) -> str:
        """Get entity name"""
        return item['odpis']["dane"]["dzial1"]["danePodmiotu"]["nazwa"]

    def jurisdiction(self, item: dict) -> str:
        """Get jurisdiction"""
        return "PL"

    @property
    def scheme(self) -> str:
        """Get scheme"""
        return 'PL-KRS'

    @property
    def scheme_name(self) -> str:
        """Get scheme name"""
        return "The National Court Register"

    def additional_identifiers(self, item: dict) -> list:
        """Get list of additional identifiers"""
        return []

    def record_id(self, item: dict) -> str:
        """Get recordID"""
        return f"PL-KRS-{int(item['odpis']['naglowekA']['numerKRS']):010d}"

    def registered_address(self, item: dict) -> dict:
        """Get registered address"""
        #return item['odpis']["dane"]["dzial1"]["danePodmiotu"]["adres"]
        return None

    def business_address(self, item: dict) -> dict:
        """Get registered address"""
        return item['odpis']["dane"]["dzial1"]["siedzibaIAdres"]["adres"]
        #return None

    def source_type(self, data: dict) -> str:
        """Get source type"""
        return ['officialRegister']

    @property
    def source_description(self) -> str:
        """Get source description"""
        return "The National Court Register (Poland)"

    def address_string(self, address: dict) -> str:
        """Get address string"""
        if address:
            address_data = []
            if "nrDomu" in address and address["nrDomu"]:
                address_data.append(address["nrDomu"])
            if  "ulica" in address and address["ulica"]:
                address_data.append(address["ulica"])
            if "miejscowosc" in address and address["miejscowosc"]:
                address_data.append(address["miejscowosc"])
            #if "region" in address and address["region"]:
            #    address_data.append(address["region"])
            return ", ".join(address_data)
        else:
            return None

    def address_country(self, address: dict) -> str:
        """Get address country"""
        return address["kraj"] if "kraj" in address else None

    def address_postcode(self, address: dict) -> Optional[str]:
        """Get address postcode"""
        return address["kodPocztowy"]

    def creation_date(self, item: dict) -> Optional[str]:
        """Get creation date"""
        creation_date = item["odpis"]["naglowekA"]["dataRejestracjiWKRS"]
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
       ident = self.indentifier(data)
       registration_status = self.registation_status(data)
       return (f"Polish National Court Register data for this entity: {ident}; Registration Status: {registration_status}",
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
        return item["odpis"]["naglowekA"]["dataOstatniegoWpisu"]

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
