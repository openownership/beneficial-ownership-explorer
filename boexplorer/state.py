from typing import List, Any

import reflex as rx

#from boexplorer.display.details import entity_details
from boexplorer.display.table import construct_table
from boexplorer.search import perform_search

class ExplorerState(rx.State):
    """The app state."""
    bods_data: dict = {}
    data_table: List = []
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

    def get_search_result(self, form_data: dict[str, str]):
        self.searching = True
        self.bods_data = perform_search(form_data["search_text"])
        self.data_table = construct_table(self.bods_data)
        print(self.data_table)
        self.searching = False
        self.display_table = True
        return rx.redirect("/results")

    def get_detail(self, pos):
        col, row = pos
        self.detail_identifier = self.data_table[row][2]
        self.detail_statement = self.bods_data[self.detail_identifier][0]
        return rx.redirect("/details")
