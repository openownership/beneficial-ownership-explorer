from functools import partial
from typing import List, Any

import reflex as rx

from boexplorer.state import ExplorerState

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

def index() -> rx.Component:
    # Landing Page (Index)
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("BO Explorer", font_size="9"),
            rx.form(
                rx.vstack(
                    rx.input(
                        id="search_text",
                        placeholder="Enter a ownership search..",
                        size="3",
                    ),
                    rx.button(
                        "Search",
                        type="submit",
                        size="3",
                    ),
                    align="stretch",
                    spacing="2",
                ),
                width="100%",
                on_submit=ExplorerState.get_search_result,
            ),
            rx.divider(),
            width="25em",
            bg="white",
            padding="2em",
            align="center",
        ),
    )

app = rx.App()
app.add_page(index)
app.add_page(results)
app.add_page(details)
