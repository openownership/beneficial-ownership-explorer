import re
from datetime import date
from typing import Optional, Tuple, Union

from parsel import Selector

from boexplorer.apis.protocol import API
from boexplorer.utils.dates import current_date
from boexplorer.download.authentication import authenticator
from boexplorer.config import app_config

class FranceINPI(API):
    """Handle accessing French INPI api"""

    @property
    def authenticator(self) -> str:
        """API authenticator"""
        return authenticator(username=app_config["sources"]["france_inpi"]["credentials"]["user"],
                             password=app_config["sources"]["france_inpi"]["credentials"]["pass"],
                             auth_type="bearer",
                             auth_url="https://registre-national-entreprises.inpi.fr/api/sso/login")

    @property
    def base_url(self) -> str:
        """API base url"""
        return "https://registre-national-entreprises.inpi.fr/api/companies"

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
                "company_persons": None,
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
        """API company persons url"""
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
        return "page", 1

    @property
    def page_size_max(self) -> int:
        """Maximum page size"""
        return 5

    def query_company_name_params(self, text) -> dict:
        """Querying company name parameter"""
        return {"companyName": text}

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

    def query_company_persons_params(self, data) -> dict:
        """Querying company name parameter"""
        return None

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
            if isinstance(json_data, list):
                return True
            else:
                return False

    def filter_result(self, data: dict, search_type=None, search=None, detail=False) -> bool:
        """Filter out item if meets condition"""
        return False

    def extract_data(self, json_data: dict) -> dict:
        """Extract main data body from json data"""
        return json_data

    def company_prepocessing(self, data: dict) -> dict:
        pass

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
        items = []
        for company in data:
            if "personneMorale" in company["formality"]["content"]:
                entity = company["formality"]["content"]["personneMorale"]
                #print("Entity:", entity)
                if "beneficiairesEffectifs" in entity:
                    for person in entity["beneficiairesEffectifs"]:
                        items.append(person)
        #print("Person items:", items)
        return items

    def extract_relationship_item(self, data: dict) -> dict:
        """Extract relationship item data"""
        return data['attributes']['relationship']

    def identifier(self, data: dict) -> str:
        """Get entity identifier"""
        return data["formality"]["siren"]

    def person_identifier(self, data: dict) -> str:
        """Get person identifier"""
        family_name = data["beneficiaire"]["descriptionPersonne"]["nom"]
        first_names = data["beneficiaire"]["descriptionPersonne"]["prenoms"]
        names = " ".join(first_names + [family_name])
        return f"FR-RCS-PER-{names.replace(' ', '-')}"

    def entity_name(self, item: dict) -> str:
        """Get entity name"""
        if "exploitation" in item["formality"]["content"]:
            return item["formality"]["content"]["exploitation"]["identite"]["entreprise"]["denomination"]
        if "personneMorale" in item["formality"]["content"]:
            return item["formality"]["content"]["personneMorale"]["identite"]["entreprise"]["denomination"]
        #["etablissementPrincipal"]["descriptionEtablissement"]["nomCommercial"]
        return None

    def jurisdiction(self, item: dict) -> str:
        """Get jurisdiction"""
        return "FR"

    @property
    def scheme(self) -> str:
        """Get scheme"""
        return 'FR-RCS'

    @property
    def search_url(self) -> str:
        """URL for manual search"""
        return 'https://registre-national-entreprises.inpi.fr/login'

    @property
    def scheme_name(self) -> str:
        """Get scheme name"""
        return 'Register of Companies (Sirene)'

    def additional_identifiers(self, item: dict) -> list:
        """Get list of additional identifiers"""
        return []

    def record_id(self, item: dict) -> str:
        """Get recordID"""
        if 'formality' in item:
            return f"FR-RCS-{item['formality']['siren']}"
        else:
            return self.person_identifier(item)

    def registered_address(self, item: dict) -> dict:
        """Get registered address"""
        if "exploitation" in item["formality"]["content"]:
            if "etablissementPrincipal" in item["formality"]["content"]["exploitation"]:
                return item["formality"]["content"]["exploitation"]["etablissementPrincipal"]["adresse"]
        if "personneMorale" in item["formality"]["content"]:
            if "etablissementPrincipal" in item["formality"]["content"]["personneMorale"]:
                return item["formality"]["content"]["personneMorale"]["etablissementPrincipal"]["adresse"]
        return None

    def business_address(self, item: dict) -> dict:
        """Get registered address"""
        if "exploitation" in item["formality"]["content"]:
            if "adresseEntreprise" in item["formality"]["content"]["exploitation"]:
                return item["formality"]["content"]["exploitation"]["adresseEntreprise"]["adresse"]
        if "personneMorale" in item["formality"]["content"]:
            if "adresseEntreprise" in item["formality"]["content"]["personneMorale"]:
                return item["formality"]["content"]["personneMorale"]["adresseEntreprise"]["adresse"]
        return None

    def source_type(self, data: dict) -> str:
        """Get source type"""
        return ['officialRegister']

    @property
    def source_description(self) -> str:
        """Get source description"""
        return 'Register of Companies (FR)'

    def address_string(self, address: dict) -> str:
        """Get address string"""
        if address:
            address_data = []
            if "numVoie" in address and address["numVoie"]:
                address_data.append(address["numVoie"])
            if "typeVoie" in address and address["typeVoie"]:
                address_data.append(address["typeVoie"])
            if "voie" in address and address["voie"]:
                address_data.append(address["voie"])
            if "commune" in address and address["commune"]:
                address_data.append(address["commune"])
            return " ".join(address_data)
        else:
            return None

    def address_country(self, address: dict) -> str:
        """Get address country"""
        return address["pays"] if "pays" in address else None

    def address_postcode(self, address: dict) -> Optional[str]:
        """Get address postcode"""
        if "codePostal" in address:
            return address["codePostal"]
        else:
            return None

    def creation_date(self, item: dict) -> Optional[str]:
        """Get creation date"""
        if "dateCreation" in item["formality"]["content"]["natureCreation"]:
            creation_date = item["formality"]["content"]["natureCreation"]["dateCreation"]
            if creation_date:
                return creation_date.split("T")[0]
            else:
                return None
        else:
            return None

    def registation_status(self, data: dict) -> str:
        """Get registation status"""
        #return data["attributes"]["registration"]["status"]
        return None

    def entity_annotation(self, data: dict) -> Tuple[str, str]:
       """Annotation of status for all entity statements (not generated as a result
       of a reporting exception)"""
       ident = self.identifier(data)
       registration_status = self.registation_status(data)
       return (f"FR Register of Companies data for this entity: {ident}; Registration Status: {registration_status}",
               "/")

    def person_annotation(self, data: dict) -> Tuple[str, str]:
        """Annotation of status for all person statements (not generated as a result of a reporting exception)"""
        ident = self.person_identifier(data)
        #registration_status = self.registation_status(data)
        return (f"FR Register of Companies data for this person: {ident}", "/")

    def person_name_components(self, item: dict) -> Tuple[str, str, str, str]:
        """Extract person name components"""
        family_name = item["beneficiaire"]["descriptionPersonne"]["nom"]
        first_names = itemdata["beneficiaire"]["descriptionPersonne"]["prenoms"]
        names = " ".join(first_names + [family_name])
        return names, family_name, first_names[0], None

    def person_birth_date(self, item: dict):
        """Extract person birth date"""
        return item["beneficiaire"]["descriptionPersonne"]["dateDeNaissance"]

    def person_tax_residency(self, item: dict):
        """Extract person tax residency"""
        if "adresseDomicile" in item["beneficiaire"] and "pays" in item["beneficiaire"]["adresseDomicile"]:
            return item["beneficiaire"]["adresseDomicile"]["pays"]
        else:
            return None

    def unspecified_person(self, item: dict):
        """Person unspecified"""
        if "nom" in item and item["nom"]:
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
        if "updatedAt" in item:
            return item["updatedAt"]
        else:
            return date.today().strftime("%Y-%m-%d")

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
