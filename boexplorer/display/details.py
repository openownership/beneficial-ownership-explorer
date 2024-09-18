import reflex as rx

from typing import Any

from boexplorer.state import ExplorerState

def address_details(address: dict) -> rx.Component:
    address_items = []
    if "address" in adresss and address["address"]:
        address_items.append(rx.list.item(f"Address: {address['address']}"))
    if "postCode" in address and address["postCode"]:
        address_items.append(rx.list.item(f"Postcode: {address['postCode']}"))
    if "country" in address and address["country"]:
        address_items.append(rx.list.item(f"Country: {address['country']}"))
    return rx.list.unordered(*address_items)

def address_card(address: dict) -> rx.Component:
    return rx.vstack(
        rx.text(f"Address ({address['type'].title()}", weight="bold", size="6"),
        address_details(address),
        spacing="6",
        border=f"1.5px solid {rx.color('gray', 5)}",
        background=rx.color("gray", 1),
        padding="28px",
        width="100%",
        max_width="400px",
        justify="center",
        border_radius="0.5rem",
    )

def entity_details_card(statement: dict[str: Any]) -> rx.Component:
    return rx.vstack(
        rx.text(f"{statement['recordDetails']['name'].title()}", weight="bold", size="8"),
        rx.text(f"{statement['recordId'].title()}", weight="bold", size="6"),
        rx.text(f"{statement['recordDetails']['foundingDate'].title()}", weight="bold", size="6"),
        spacing="6",
        border=f"1.5px solid {rx.color('gray', 5)}",
        background=rx.color("gray", 1),
        padding="28px",
        width="100%",
        max_width="400px",
        justify="center",
        border_radius="0.5rem",
    )

def entity_details() -> rx.Component:
    statement = ExplorerState.detail_statement
    return rx.grid(
        entity_details_card(statement),
        rx.foreach(statement['recordDetails']["addresses"], address_card),
        columns="2",
    )
