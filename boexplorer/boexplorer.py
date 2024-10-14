from functools import partial
from typing import List, Any

import reflex as rx

from boexplorer import style
from boexplorer.layout.navbar import navbar
from boexplorer.state import ExplorerState
from boexplorer.components.table import summary_table

def details() -> rx.Component:
    # Details Page
    return rx.container(
        #rx.text(ExplorerState.detail_identifier)
        #entity_details()
    )

def results() -> rx.Component:
    # Results Page
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.cond(
                ExplorerState.searching,
                rx.chakra.circular_progress(is_indeterminate=True),
                rx.cond(
                    ExplorerState.display_table,
                    #rx.data_table(
                    #    data=State.data_table,
                    #    columns=State.columns,
                    #    pagination=True,
                    #    search=True,
                    #    sort=True,
                    #)
                    rx.data_editor(
                        columns=ExplorerState.columns,
                        data=ExplorerState.data_table,
                        on_cell_clicked=ExplorerState.get_detail,
                    )
                ),
            ),
            width="100em",
            bg="white",
            padding="2em",
            align="center",
        ),
    )


def company_results() -> rx.Component:
    """Results page"""
    return rx.fragment(
               rx.vstack(
                   navbar(title="Beneficial Ownership Explorer"),
                   rx.center(
                       rx.color_mode.button(position="bottom-left"),
                       rx.cond(
                           ExplorerState.display_table,
                           summary_table(ExplorerState.data_table)
                       ),
                       width="100%",
                       margin="1em",
                   ),
               ),
           )

def persons_results() -> rx.Component:
    """Results page"""
    return rx.fragment(
               rx.vstack(
                   navbar(title="Beneficial Ownership Explorer"),
                   rx.center(
                       rx.color_mode.button(position="bottom-left"),
                       rx.cond(
                           ExplorerState.display_table,
                           summary_table(ExplorerState.data_table)
                       ),
                       width="100%",
                       margin="1em",
                   ),
               ),
           )

def search_bar() -> rx.Component:
    """Search bar"""
    return rx.vstack(
        rx.input(
            placeholder="Enter a ownership search..",
            id="search_text",
            style=style.input_style,
        ),
        rx.radio(
            ["Company search", "Person search"],
            default_value="Company search",
            name="search_type",
            required=True,
            direction="row",
            spacing="9"
        ),
        rx.button(
            "Search",
            type="submit",
            style=style.button_style,
        ),
    )

def search_form() -> rx.Component:
    """Search form"""
    return rx.center(
        rx.form(
            rx.vstack(
                search_bar(),
                align="center",
            ),
            on_submit=ExplorerState.get_search_result,
        )
    )

def index() -> rx.Component:
    """Search page"""
    return rx.fragment(
               rx.vstack(
                   navbar(title="Beneficial Ownership Explorer"),
                   rx.container(
                       rx.color_mode.button(position="bottom-left"),
                       rx.center(
                           rx.cond(
                               ExplorerState.searching,
                               rx.spinner(size="3"),
                               rx.hstack(
                                   #sidebar(),
                                   rx.box(
                                       search_form(),
                                       padding="1em",
                                       width="100%",
                                       align="center",
                                  ),
                                  width="100%",
                               ),
                           ),
                           width="100%",
                       ),
                       size="4",
                   ),
               ),
           )

def index() -> rx.Component:
    """Search page"""
    return rx.fragment(
               rx.vstack(
                   navbar(title="Beneficial Ownership Explorer"),
                   rx.center(
                      rx.cond(
                           ExplorerState.searching,
                           rx.vstack(
                               rx.center(rx.spinner(size="3"),
                                         width="100%"),
                               rx.text("Searching..."),
                           ),
                           search_form(),
                       ),
                       width="100%",
                       margin="1em",
                   )
               )
           )

app = rx.App()
app.add_page(index, on_load=ExplorerState.initialise_search_page)
app.add_page(company_results, route="/companies")
app.add_page(persons_results, route="/persons")
app.add_page(details)
