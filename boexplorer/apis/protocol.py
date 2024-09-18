from abc import abstractmethod, abstractproperty
from typing import Optional, Protocol, Tuple, Union, runtime_checkable


@runtime_checkable
class API(Protocol):

    @abstractproperty
    def authenticator(self) -> str:
        """API authenticator"""

    @abstractproperty
    def base_url(self) -> str:
        """API base url"""

    @abstractproperty
    def http_post(self) -> dict:
        """API http post"""

    @abstractproperty
    def post_pagination(self) -> bool:
        """API post pagination"""

    @abstractproperty
    def company_search_url(self) -> str:
        """API company search url"""

    @abstractmethod
    def company_detail_url(self, company_data: dict) -> str:
        """API company detail url"""

    @abstractmethod
    def to_local_characters(self, text):
        """Transliterate into local characters"""

    @abstractmethod
    def from_local_characters(self, text):
        """Transliterate from local characters"""

    @abstractproperty
    def page_size_par(self) -> Tuple[str, bool]:
        """Page size parameter"""

    @abstractproperty
    def page_number_par(self) -> Tuple[str, int]:
        """Page number parameter"""

    @abstractproperty
    def page_size_max(self) -> int:
        """Maximum page size"""

    @abstractmethod
    def query_company_name_params(self, text: str) -> dict:
        """Querying company name parameters"""

    @abstractproperty
    def query_company_name_extra(self) -> str:
        """Querying company name extra parameters"""

    @abstractproperty
    def query_company_detail_params(self, company_data: dict) -> dict:
        """Querying company detail parameters"""

    @abstractproperty
    def query_company_detail_extra(self) -> str:
        """Querying company details extra parameters"""

    @abstractmethod
    def query_person_name_params(self, text) -> dict:
        """Querying person name parameter"""

    @abstractproperty
    def query_person_name_extra(self) -> str:
        """Querying person name extra parameters"""

    @abstractmethod
    def check_result(self, json_data: Union[dict, list]) -> bool:
        """Check successful return value"""

    @abstractmethod
    def filter_result(self, data: dict, detail=False) -> bool:
        """Filter out item if meets condition"""

    @abstractmethod
    def extract_data(self, json_data: dict) -> dict:
        """Extract main data body from json data"""

    @abstractmethod
    def extract_type(self, json_data: dict) -> Optional[str]:
        """Extract item type (entity, relationship or exception)"""

    @abstractmethod
    def extract_entity_item(self, data: dict) -> dict:
        """Extract relationship item data"""

    @abstractmethod
    def extract_relationship_item(self, data: dict) -> dict:
        """Extract relationship item data"""

    @abstractmethod
    def indentifier(self, data: dict) -> str:
        """Get entity identifier"""

    @abstractmethod
    def entity_name(self, item: dict) -> str:
        """Get entity name"""

    @abstractmethod
    def jurisdiction(self, item: dict) -> str:
        """Get jurisdiction"""

    @abstractproperty
    def scheme(self) -> str:
        """Get scheme"""

    @abstractproperty
    def scheme_name(self) -> str:
        """Get scheme name"""

    @abstractmethod
    def additional_identifiers(self, item: dict) -> list:
        """Get list of additional identifiers"""

    @abstractmethod
    def record_id(self, item: dict) -> str:
        """Get recordID"""

    @abstractmethod
    def registered_address(self, item: dict) -> dict:
        """Get registered address"""

    @abstractmethod
    def business_address(self, item: dict) -> dict:
        """Get registered address"""

    @abstractmethod
    def address_string(self, address: dict) -> str:
        """Get address string"""

    @abstractmethod
    def address_country(self, address: dict) -> str:
        """Get address country"""

    @abstractmethod
    def address_postcode(self, address: dict) -> Optional[str]:
        """Get address postcode"""

    @abstractmethod
    def creation_date(self, item: dict) -> Optional[str]:
        """Get creation date"""

    @abstractmethod
    def source_type(self, data: dict) -> str:
        """Get source type"""

    @abstractproperty
    def source_description(self) -> str:
        """Get source description"""

    @abstractmethod
    def registation_status(self, data: dict) -> str:
        """Get registation status"""

    @abstractmethod
    def entity_annotation(self, data: dict) -> Tuple[str, str]:
        """Annotation of entity statements"""

    @abstractmethod
    def subject_id(self, item: dict) -> str:
        """Get relationship subject identifier"""

    @abstractmethod
    def interested_id(self, item: dict) -> str:
        """Get relationship interested party identifier"""

    @abstractmethod
    def relationship_type(self, item: dict) -> str:
        """Get relationship type"""

    @abstractmethod
    def update_date(self, item: dict) -> str:
        """Get update date"""

    @abstractmethod
    def interest_details(self, item: dict) -> str:
        """Get interest details"""

    @abstractmethod
    def extract_links(self, data: dict) -> dict:
        """Extract links"""
