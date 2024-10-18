from typing import List, Any

import reflex as rx

#from boexplorer.display.details import entity_details
from boexplorer.display.table import construct_company_table, construct_summary_table, summary_columns
from boexplorer.search import perform_company_search, perform_person_search

class ExplorerState(rx.State):
    """The app state."""
    bods_data: dict = {}
    data_table: List[List[str]] = []
    summary_columns: List[str] = ["Source", "Country", "Companies", "Individuals", "Links"]
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
            bods_data = await perform_company_search(form_data["search_text"])
            #self.data_table = construct_company_table(self.bods_data)
            columns = summary_columns(table_type="company")
            data_table = construct_summary_table(bods_data, table_type="company")
            print(data_table)
            async with self:
                self.bods_data = bods_data
                self.summary_columns = columns
                self.data_table = data_table
                self.display_table = True
            return rx.redirect("/companies")
        else:
            bods_data = await perform_person_search(form_data["search_text"])
            columns = summary_columns(table_type="person")
            data_table = construct_summary_table(bods_data, table_type="person")
            async with self:
                self.bods_data = bods_data
                self.summary_columns = columns
                self.data_table = data_table
                self.display_table = True
            return rx.redirect("/persons")

    def get_detail(self, pos):
        col, row = pos
        self.detail_identifier = self.data_table[row][2]
        self.detail_statement = self.bods_data[self.detail_identifier][0]
        return rx.redirect("/details")

    def initialise_search_page(self):
        self.searching = False
