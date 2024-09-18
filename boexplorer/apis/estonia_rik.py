import re
from typing import Optional, Tuple, Union

from parsel import Selector

from boexplorer.apis.protocol import API
from boexplorer.utils.dates import current_date
from boexplorer.download.authentication import authenticator

class EstoniaRIK(API):
    """Handle accessing Estonian RIK api"""

    @property
    def authenticator(self) -> str:
        """API authenticator"""
        return {"user": "EVANSMIRANDA", "pass": "valued*smack9HOSANNAH"}

    @property
    def base_url(self) -> str:
        """API base url"""
        return "https://ariregxmlv6.rik.ee"

    @property
    def http_post(self) -> dict:
        """API http post"""
        return {"company_search": True,
                "company_detail": None}

    @property
    def post_pagination(self) -> bool:
        """API post pagination"""
        return False

    @property
    def company_search_url(self) -> str:
        """API company search url"""
        return f"{self.base_url}"

    def company_detail_url(self, company_data) -> str:
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
        return None, False

    @property
    def page_number_par(self) -> Tuple[str, int]:
        """Page number parameter"""
        return None, 0

    @property
    def page_size_max(self) -> int:
        """Maximum page size"""
        return 10

    def query_company_name_params(self, text) -> dict:
        """Querying company name parameter"""
        soap_query_start='''<?xml version="1.0" encoding="UTF-8"?>
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
        xmlns:iden="http://x-road.eu/xsd/identifiers"
        xmlns:prod="http://arireg.x-road.eu/producer/" xmlns:xro="http://x-road.eu/xsd/xroad.xsd">
        <soapenv:Body>
        <prod:lihtandmed_v2>
        <prod:keha>'''
        soap_user=f"<prod:ariregister_kasutajanimi>{self.authenticator['user']}</prod:ariregister_kasutajanimi>"
        soap_pass=f"<prod:ariregister_parool>{self.authenticator['pass']}</prod:ariregister_parool>"
        soap_query_company_name = f"<prod:evnimi>{text}</prod:evnimi>"
        soap_query_end='''<prod:ariregister_valjundi_formaat>json</prod:ariregister_valjundi_formaat>
        <prod:keel>eng</prod:keel>
        <prod:evarv>10</prod:evarv>
        </prod:keha>
        </prod:lihtandmed_v2>
        </soapenv:Body>
        </soapenv:Envelope>'''
        return soap_query_start + soap_user + soap_pass + soap_query_company_name + soap_query_end

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
        return {}

    def check_result(self, json_data: Union[dict, list], detail=False) -> bool:
        """Check successful return value"""
        if detail:
            if isinstance(json_data, dict) and "companyName" in json_data:
                return True
            else:
                return False
        else:
            if "keha" in json_data:
                return True
            else:
                return False

    def filter_result(self, data: dict, detail=False) -> bool:
        """Filter out item if meets condition"""
        return False

    def extract_data(self, json_data: dict) -> dict:
        """Extract main data body from json data"""
        return json_data["keha"]["ettevotjad"]["item"]

    def company_prepocessing(self, data: dict) -> dict:
        pass

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

    def extract_relationship_item(self, data: dict) -> dict:
        """Extract relationship item data"""
        return data['attributes']['relationship']

    def indentifier(self, data: dict) -> str:
        """Get entity identifier"""
        return data["ariregistri_kood"]

    def entity_name(self, item: dict) -> str:
        """Get entity name"""
        return item["evnimi"]

    def jurisdiction(self, item: dict) -> str:
        """Get jurisdiction"""
        return "EE"

    @property
    def scheme(self) -> str:
        """Get scheme"""
        return "EE-RIK"

    @property
    def scheme_name(self) -> str:
        """Get scheme name"""
        return "Centre of Registers and Information Systems (RIK)"

    def additional_identifiers(self, item: dict) -> list:
        """Get list of additional identifiers"""
        return []

    def record_id(self, item: dict) -> str:
        """Get recordID"""
        return f"EE-RIK-{item['ariregistri_kood']}"

    def registered_address(self, item: dict) -> dict:
        """Get registered address"""
        return None

    def business_address(self, item: dict) -> dict:
        """Get registered address"""
        return item["evaadressid"]

    def source_type(self, data: dict) -> str:
        """Get source type"""
        return ['officialRegister']

    @property
    def source_description(self) -> str:
        """Get source description"""
        return "Centre of Registers and Information Systems (EE)"

    def address_string(self, address: dict) -> str:
        """Get address string"""
        if address:
            address_data = []
            if  "aadress_ads__ads_normaliseeritud_taisaadress" in address and address["aadress_ads__ads_normaliseeritud_taisaadress"]:
                address_data.append(address["aadress_ads__ads_normaliseeritud_taisaadress"])
            #if "by" in address and address["by"]:
            #    address_data.append(address["by"])
            #if "region" in address and address["region"]:
            #    address_data.append(address["region"])
            return ", ".join(address_data)
        else:
            return None

    def address_country(self, address: dict) -> str:
        """Get address country"""
        return address["aadress_riik_tekstina"] if "aadress_riik_tekstina" in address else None

    def address_postcode(self, address: dict) -> Optional[str]:
        """Get address postcode"""
        return None

    def creation_date(self, item: dict) -> Optional[str]:
        """Get creation date"""
        creation_date = item["esmakande_aeg"]
        if creation_date:
            return creation_date.split("T")[0]
        else:
            return None

    def registation_status(self, data: dict) -> str:
        """Get registation status"""
        if data["staatus"]== "R":
            return "Registered"
        elif data["staatus"] == "L":
            return "Liquidation"
        elif data["staatus"] == "N":
            return "Bankrupt"
        elif data["staatus"] == "K":
            return "Deleted"
        return None

    def entity_annotation(self, data: dict) -> Tuple[str, str]:
       """Annotation of status for all entity statements (not generated as a result
       of a reporting exception)"""
       ident = self.indentifier(data)
       registration_status = self.registation_status(data)
       return (f"DK Central Business Register data for this entity: {ident}; Registration Status: {registration_status}",
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
