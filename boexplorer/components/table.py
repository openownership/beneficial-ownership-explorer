from typing import List
import reflex as rx

def summary_table_header():
    return rx.table.header(
            rx.table.row(
                rx.table.column_header_cell("Country"),
                rx.table.column_header_cell("Source"),
                rx.table.column_header_cell("Companies"),
                rx.table.column_header_cell("Individuals"),
                rx.table.column_header_cell("Links")
            ),
        )

def summary_table_row(row: List[str]):
    """Show table row."""
    return rx.table.row(
        rx.table.cell(row[0]),
        rx.table.cell(row[1]),
        rx.table.cell(row[2]),
        rx.table.cell(row[3]),
        rx.table.cell(rx.link(f"Search {row[1]}", href=row[4])),
    )

def summary_table(rows: List[List[str]]):
    return rx.table.root(
        summary_table_header(),
        rx.table.body(
            rx.foreach(
                rows, summary_table_row
            )
        ),
        width="100%",
    )
