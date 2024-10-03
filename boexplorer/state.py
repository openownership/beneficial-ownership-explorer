from typing import List, Any

import reflex as rx

#from boexplorer.display.details import entity_details
from boexplorer.display.table import construct_company_table, construct_summary_table
from boexplorer.search import perform_company_search, perform_person_search

class ExplorerState(rx.State):
    """The app state."""
    bods_data: dict = {}
    data_table: List = []
    summary_columns: List[str] = ["Source", "Country", "Companies", "Individuals"]
    columns: list[Any] = [
        {
            "title": "Name",
            "type": "str",
        },
        {
            "title": "Incorporated",
            "type": "str",
        },
        {
            "title": "Identifier",
            "type": "str",
        },
        {
            "title": "Founding",
            "type": "str",
        },
        {
            "title": "Source",
            "type": "str",
        }
    ]
    searching: bool = False
    display_table: bool = False
    detail_identifier: str = ""
    detail_statement: dict = {}

    @rx.background
    async def get_search_result(self, form_data: dict[str, str]):
        print("Form data:", form_data)
        async with self:
            self.searching = True
        if form_data["search_type"] == 'Company search':
            bods_data = perform_company_search(form_data["search_text"])
            #self.data_table = construct_company_table(self.bods_data)
            data_table = construct_summary_table(bods_data)
            print(data_table)
            async with self:
                self.bods_data = bods_data
                self.data_table = data_table
                self.searching = False
                self.display_table = True
            return rx.redirect("/companies")
        else:
            bods_data = perform_person_search(form_data["search_text"])
            data_table = construct_summary_table(bods_data)
            async with self:
                self.bods_data = bods_data
                self.data_table = data_table
                self.searching = False
                self.display_table = True
            return rx.redirect("/persons")

    def get_detail(self, pos):
        col, row = pos
        self.detail_identifier = self.data_table[row][2]
        self.detail_statement = self.bods_data[self.detail_identifier][0]
        return rx.redirect("/details")
